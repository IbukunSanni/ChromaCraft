from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from starlette.concurrency import run_in_threadpool
import numpy as np
import gc

# ✅ Load small model once globally
print("🧠 Loading transformer model...")
model = SentenceTransformer("paraphrase-albert-small-v2")
print("✅ Model loaded.")

# ✅ Cache reference concept encodings once
REFERENCE_ENCODINGS = {
    label: model.encode(label)
    for label in ["bright", "dark", "warm", "cool", "saturated", "desaturated"]
}


# Import color utilities
from utils.color_utils import (
    hex_to_rgb_normalized,
    rgb_normalized_to_hex,
    adjust_hue,
    adjust_saturation
)


# 🧠 Encode concept string → vector (offloaded to threadpool)
async def concept_vector(concept: str):
    return await run_in_threadpool(model.encode, concept)


# ✅ Compute similarity weights for a given concept
async def get_adjustment_weights(concept: str):
    vec = await concept_vector(concept)
    weights = {}
    for key, ref_vec in REFERENCE_ENCODINGS.items():
        sim = np.dot(vec, ref_vec) / (np.linalg.norm(vec) * np.linalg.norm(ref_vec))
        weights[key] = sim
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
