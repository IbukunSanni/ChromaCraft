"""
Color harmony algorithms for generating harmonious color palettes.
Implements complementary, triadic, analogous, and other color theory rules.
"""

import random
from typing import List, Tuple
from math import cos, sin, pi
from utils.color_utils import hex_to_hsl, hsl_to_hex, normalize_hue


def generate_complementary_palette(
    base_hue: float, saturation: float, lightness: float
) -> List[str]:
    """Generate a 5-color complementary palette."""
    colors = []

    # Base color
    colors.append(hsl_to_hex(base_hue, saturation, lightness))

    # Complementary color (180 degrees opposite)
    comp_hue = normalize_hue(base_hue + 0.5)
    colors.append(hsl_to_hex(comp_hue, saturation, lightness))

    # Add variations with different lightness
    colors.append(hsl_to_hex(base_hue, saturation * 0.7, min(lightness + 0.2, 0.9)))
    colors.append(hsl_to_hex(comp_hue, saturation * 0.7, min(lightness + 0.2, 0.9)))
    colors.append(hsl_to_hex(base_hue, saturation * 0.5, max(lightness - 0.3, 0.1)))

    return colors


def generate_triadic_palette(
    base_hue: float, saturation: float, lightness: float
) -> List[str]:
    """Generate a 5-color triadic palette."""
    colors = []

    # Three main colors 120 degrees apart
    hues = [base_hue, normalize_hue(base_hue + 1 / 3), normalize_hue(base_hue + 2 / 3)]

    for hue in hues:
        colors.append(hsl_to_hex(hue, saturation, lightness))

    # Add two variations
    colors.append(hsl_to_hex(hues[0], saturation * 0.6, min(lightness + 0.25, 0.9)))
    colors.append(hsl_to_hex(hues[1], saturation * 0.6, max(lightness - 0.25, 0.1)))

    return colors


def generate_analogous_palette(
    base_hue: float, saturation: float, lightness: float
) -> List[str]:
    """Generate a 5-color analogous palette."""
    colors = []

    # Five colors within 60 degrees of each other
    hue_offsets = [-0.08, -0.04, 0, 0.04, 0.08]  # About 30 degrees each way

    for offset in hue_offsets:
        hue = normalize_hue(base_hue + offset)
        # Vary saturation and lightness slightly for interest
        s_variation = random.uniform(0.8, 1.2)
        l_variation = random.uniform(0.8, 1.2)
        final_s = min(max(saturation * s_variation, 0.1), 1.0)
        final_l = min(max(lightness * l_variation, 0.1), 0.9)
        colors.append(hsl_to_hex(hue, final_s, final_l))

    return colors


def generate_tetradic_palette(
    base_hue: float, saturation: float, lightness: float
) -> List[str]:
    """Generate a 5-color tetradic (square) palette."""
    colors = []

    # Four colors 90 degrees apart
    hues = [
        base_hue,
        normalize_hue(base_hue + 0.25),
        normalize_hue(base_hue + 0.5),
        normalize_hue(base_hue + 0.75),
    ]

    for hue in hues:
        colors.append(hsl_to_hex(hue, saturation, lightness))

    # Add one neutral variation
    colors.append(hsl_to_hex(base_hue, saturation * 0.3, 0.5))

    return colors


def generate_monochromatic_palette(
    base_hue: float, saturation: float, lightness: float
) -> List[str]:
    """Generate a 5-color monochromatic palette."""
    colors = []

    # Five variations of the same hue with different saturation and lightness
    lightness_values = [0.2, 0.4, lightness, min(lightness + 0.3, 0.8), 0.9]
    saturation_values = [
        saturation,
        saturation * 0.8,
        saturation * 0.6,
        saturation * 0.4,
        saturation * 0.2,
    ]

    for i in range(5):
        colors.append(hsl_to_hex(base_hue, saturation_values[i], lightness_values[i]))

    return colors


def generate_split_complementary_palette(
    base_hue: float, saturation: float, lightness: float
) -> List[str]:
    """Generate a 5-color split-complementary palette."""
    colors = []

    # Base color
    colors.append(hsl_to_hex(base_hue, saturation, lightness))

    # Two colors adjacent to the complement
    comp_hue = normalize_hue(base_hue + 0.5)
    colors.append(hsl_to_hex(normalize_hue(comp_hue - 0.08), saturation, lightness))
    colors.append(hsl_to_hex(normalize_hue(comp_hue + 0.08), saturation, lightness))

    # Add variations
    colors.append(hsl_to_hex(base_hue, saturation * 0.7, min(lightness + 0.2, 0.9)))
    colors.append(hsl_to_hex(base_hue, saturation * 0.4, max(lightness - 0.3, 0.1)))

    return colors


HARMONY_GENERATORS = {
    "complementary": generate_complementary_palette,
    "triadic": generate_triadic_palette,
    "analogous": generate_analogous_palette,
    "tetradic": generate_tetradic_palette,
    "monochromatic": generate_monochromatic_palette,
    "split_complementary": generate_split_complementary_palette,
}


def generate_random_harmonious_palette(
    harmony_type: str = None, locked_colors: List[str] = None
) -> List[str]:
    """
    Generate a random harmonious color palette with support for locked colors.

    Args:
        harmony_type: Type of harmony ('complementary', 'triadic', 'analogous', etc.)
                     If None, randomly selects one.
        locked_colors: List of HEX colors to keep unchanged

    Returns:
        List of 5 HEX color strings
    """
    if locked_colors is None:
        locked_colors = []

    # If we have locked colors, use the first one as base for harmony
    if locked_colors:
        base_hue, base_saturation, base_lightness = hex_to_hsl(locked_colors[0])
    else:
        # Generate random base color
        base_hue = random.random()
        base_saturation = random.uniform(0.4, 0.9)
        base_lightness = random.uniform(0.3, 0.7)

    # Select harmony type
    if harmony_type is None or harmony_type not in HARMONY_GENERATORS:
        harmony_type = random.choice(list(HARMONY_GENERATORS.keys()))

    # Generate palette
    generator = HARMONY_GENERATORS[harmony_type]
    palette = generator(base_hue, base_saturation, base_lightness)

    # Create a new palette that preserves locked colors in their original positions
    # This is more complex but ensures locked colors stay where they were
    if locked_colors:
        # For now, we'll use a simple approach: replace the first N colors with locked colors
        # In a more sophisticated implementation, we'd track original positions
        for i, locked_color in enumerate(locked_colors):
            if i < len(palette):
                palette[i] = locked_color

    return palette[:5]  # Ensure we return exactly 5 colors


def validate_color_harmony(colors: List[str], harmony_type: str) -> dict:
    """
    Validate if a palette follows color harmony rules.

    Args:
        colors: List of HEX color strings
        harmony_type: Expected harmony type

    Returns:
        Dictionary with validation results
    """
    if len(colors) < 2:
        return {
            "valid": False,
            "reason": "Need at least 2 colors for harmony validation",
        }

    hsl_colors = [hex_to_hsl(color) for color in colors]
    hues = [hsl[0] for hsl in hsl_colors]

    validation_result = {
        "valid": True,
        "harmony_type": harmony_type,
        "confidence": 0.0,
        "details": {},
    }

    if harmony_type == "complementary":
        # Check if colors are roughly opposite on color wheel
        if len(hues) >= 2:
            hue_diff = abs(hues[0] - hues[1])
            if hue_diff > 0.5:
                hue_diff = 1 - hue_diff
            complementary_score = 1 - abs(hue_diff - 0.5) * 2
            validation_result["confidence"] = complementary_score
            validation_result["details"]["hue_difference"] = hue_diff

    elif harmony_type == "triadic":
        # Check if colors are roughly 120 degrees apart
        if len(hues) >= 3:
            expected_gaps = [1 / 3, 1 / 3]
            actual_gaps = []
            sorted_hues = sorted(hues[:3])
            for i in range(len(sorted_hues)):
                next_i = (i + 1) % len(sorted_hues)
                gap = sorted_hues[next_i] - sorted_hues[i]
                if gap < 0:
                    gap += 1
                actual_gaps.append(gap)

            triadic_score = (
                1
                - sum(
                    abs(actual - expected)
                    for actual, expected in zip(actual_gaps, expected_gaps)
                )
                / 2
            )
            validation_result["confidence"] = max(0, triadic_score)
            validation_result["details"]["hue_gaps"] = actual_gaps

    elif harmony_type == "analogous":
        # Check if colors are close to each other on color wheel
        if len(hues) >= 2:
            max_spread = max(hues) - min(hues)
            if max_spread > 0.5:  # Handle wrap-around
                max_spread = 1 - max_spread
            analogous_score = 1 - max_spread * 6  # Penalize spreads > 1/6 (60 degrees)
            validation_result["confidence"] = max(0, analogous_score)
            validation_result["details"]["hue_spread"] = max_spread

    return validation_result
