import gc
import threading

import numpy as np
from starlette.concurrency import run_in_threadpool

# Import color utilities
from utils.color_utils import (
    hex_to_rgb_normalized,
    rgb_normalized_to_hex,
    adjust_hue,
    adjust_saturation
)

MODEL_REPO = "sentence-transformers/paraphrase-albert-small-v2"
# The model's own sentence-transformers config: mean pooling over the tokens,
# no normalization, inputs truncated to 100 tokens. Changing any of these
# changes the vectors and so every concept weight.
MAX_SEQ_LENGTH = 100
REFERENCE_LABELS = ["bright", "dark", "warm", "cool", "saturated", "desaturated"]


class OnnxSentenceEncoder:
    """The same model sentence-transformers would load, run through ONNX Runtime.

    The model repo ships an ONNX export of the transformer and a fast
    tokenizer, so torch is not needed at all. The pooling step that
    sentence-transformers would add is done here in numpy.
    """

    def __init__(self, repo_id: str = MODEL_REPO):
        from huggingface_hub import hf_hub_download
        import onnxruntime as ort
        from tokenizers import Tokenizer

        self._tokenizer = Tokenizer.from_file(hf_hub_download(repo_id, "tokenizer.json"))
        self._tokenizer.enable_truncation(max_length=MAX_SEQ_LENGTH)
        self._tokenizer.no_padding()
        self._session = ort.InferenceSession(
            hf_hub_download(repo_id, "onnx/model.onnx"),
            providers=["CPUExecutionProvider"],
        )
        self._input_names = {i.name for i in self._session.get_inputs()}

    def encode(self, text: str) -> np.ndarray:
        enc = self._tokenizer.encode(text)
        mask = np.array([enc.attention_mask], dtype=np.int64)
        feeds = {
            "input_ids": np.array([enc.ids], dtype=np.int64),
            "attention_mask": mask,
            "token_type_ids": np.array([enc.type_ids], dtype=np.int64),
        }
        hidden = self._session.run(
            None, {k: v for k, v in feeds.items() if k in self._input_names}
        )[0]
        # Mean over real tokens only: padding must not pull the average.
        weights = mask[..., None].astype(np.float32)
        pooled = (hidden * weights).sum(axis=1) / np.clip(weights.sum(axis=1), 1e-9, None)
        return pooled[0]


# The model is loaded on first use rather than at import time, so the API starts
# quickly and endpoints that do not need it (health, harmony generation, image
# extraction, export) never pay for it.
_model = None
_reference_encodings = None
_model_lock = threading.Lock()


def _load_model():
    """Load the encoder and reference encodings once (thread-safe)."""
    global _model, _reference_encodings
    if _model is None:
        with _model_lock:
            if _model is None:
                print("🧠 Loading ONNX sentence encoder...")
                model = OnnxSentenceEncoder()
                _reference_encodings = {
                    label: model.encode(label) for label in REFERENCE_LABELS
                }
                _model = model
                print("✅ Model loaded.")
    return _model, _reference_encodings


def _encode_with_references(concept: str):
    model, reference_encodings = _load_model()
    return model.encode(concept), reference_encodings


# 🧠 Encode concept string → vector (offloaded to threadpool)
async def concept_vector(concept: str):
    vec, _ = await run_in_threadpool(_encode_with_references, concept)
    return vec


# ✅ Compute similarity weights for a given concept
async def get_adjustment_weights(concept: str):
    vec, reference_encodings = await run_in_threadpool(_encode_with_references, concept)
    weights = {}
    for key, ref_vec in reference_encodings.items():
        sim = np.dot(vec, ref_vec) / (np.linalg.norm(vec) * np.linalg.norm(ref_vec))
        weights[key] = float(sim)
    del vec
    gc.collect()
    return weights


# 🎯 Adjust palette using precomputed weights (SYNC function)
def adjust_palette_by_concept(base_colors, weights):
    def adjust_color(hex_color):
        r, g, b = hex_to_rgb_normalized(hex_color)

        if weights["dark"] > 0.5:
            factor = 1 - weights["dark"] * 0.4
            r *= factor
            g *= factor
            b *= factor

        if weights["bright"] > 0.5:
            factor = weights["bright"] * 0.4
            r += (1 - r) * factor
            g += (1 - g) * factor
            b += (1 - b) * factor

        shift = (
            0.03 * weights["warm"]
            if weights["warm"] > weights["cool"]
            else -0.03 * weights["cool"]
        )
        r, g, b = adjust_hue(r, g, b, shift)

        if weights["saturated"] > weights["desaturated"]:
            sat_factor = 1 + (weights["saturated"] - weights["desaturated"]) * 0.5
        else:
            sat_factor = 1 - (weights["desaturated"] - weights["saturated"]) * 0.5
        r, g, b = adjust_saturation(r, g, b, sat_factor)

        return rgb_normalized_to_hex(r, g, b)

    print(f"🎨 Concept Weights: {weights}")
    return [adjust_color(c) for c in base_colors]
