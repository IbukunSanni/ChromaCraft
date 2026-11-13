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

MODEL_NAME = "paraphrase-albert-small-v2"
REFERENCE_LABELS = ["bright", "dark", "warm", "cool", "saturated", "desaturated"]

# The sentence-transformer model (and torch) is loaded on first use rather than
# at import time, so the API starts quickly and endpoints that do not need it
# (health, harmony generation, image extraction, export) never pay for it.
_model = None
_reference_encodings = None
_model_lock = threading.Lock()


def _load_model():
    """Load the transformer model and reference encodings once (thread-safe)."""
    global _model, _reference_encodings
    if _model is None:
        with _model_lock:
            if _model is None:
                from sentence_transformers import SentenceTransformer

                print("🧠 Loading transformer model...")
                model = SentenceTransformer(MODEL_NAME)
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
