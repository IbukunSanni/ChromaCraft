"""
Unit tests for color harmony algorithms and palette generation.
"""

import pytest
from utils.color_harmony import (
    hex_to_hsl,
    hsl_to_hex,
    normalize_hue,
    generate_complementary_palette,
    generate_triadic_palette,
    generate_analogous_palette,
    generate_tetradic_palette,
    generate_monochromatic_palette,
    generate_split_complementary_palette,
    generate_random_harmonious_palette,
    validate_color_harmony,
    HARMONY_GENERATORS,
)


class TestColorConversion:
    """Test color conversion utilities."""

    def test_hex_to_hsl_conversion(self):
        """Test HEX to HSL conversion."""
        # Test pure red
        h, s, l = hex_to_hsl("#ff0000")
        assert abs(h - 0.0) < 0.01  # Red is at 0 degrees
        assert s > 0.9  # High saturation
        assert abs(l - 0.5) < 0.1  # Medium lightness

        # Test pure blue
        h, s, l = hex_to_hsl("#0000ff")
        assert abs(h - 2 / 3) < 0.01  # Blue is at 240 degrees (2/3 of circle)
        assert s > 0.9  # High saturation

        # Test white
        h, s, l = hex_to_hsl("#ffffff")
        assert abs(l - 1.0) < 0.01  # Maximum lightness
        assert s < 0.01  # No saturation

        # Test black
        h, s, l = hex_to_hsl("#000000")
        assert abs(l - 0.0) < 0.01  # Minimum lightness

    def test_hsl_to_hex_conversion(self):
        """Test HSL to HEX conversion."""
        # Test round-trip conversion
        original = "#ff6b35"
        h, s, l = hex_to_hsl(original)
        converted = hsl_to_hex(h, s, l)

        # Should be very close (allowing for rounding)
        orig_rgb = tuple(int(original[i : i + 2], 16) for i in (1, 3, 5))
        conv_rgb = tuple(int(converted[i : i + 2], 16) for i in (1, 3, 5))

        for orig, conv in zip(orig_rgb, conv_rgb):
            assert abs(orig - conv) <= 1  # Allow 1 unit difference due to rounding

    def test_normalize_hue(self):
        """Test hue normalization."""
        assert normalize_hue(0.5) == 0.5
        assert normalize_hue(1.5) == 0.5
        assert normalize_hue(-0.5) == 0.5
        assert normalize_hue(2.0) == 0.0
        assert normalize_hue(-1.0) == 0.0


class TestHarmonyGeneration:
    """Test color harmony generation algorithms."""

    def test_complementary_palette(self):
        """Test complementary palette generation."""
        palette = generate_complementary_palette(0.0, 0.8, 0.5)  # Red base

        assert len(palette) == 5
        assert all(color.startswith("#") for color in palette)
        assert all(len(color) == 7 for color in palette)

        # Check that we have complementary colors
        base_h, _, _ = hex_to_hsl(palette[0])
        comp_h, _, _ = hex_to_hsl(palette[1])

        # Complementary colors should be ~180 degrees apart
        hue_diff = abs(base_h - comp_h)
        if hue_diff > 0.5:
            hue_diff = 1 - hue_diff
        assert abs(hue_diff - 0.5) < 0.1

    def test_triadic_palette(self):
        """Test triadic palette generation."""
        palette = generate_triadic_palette(0.0, 0.8, 0.5)

        assert len(palette) == 5
        assert all(color.startswith("#") for color in palette)

        # Check that first three colors are roughly 120 degrees apart
        hues = [hex_to_hsl(color)[0] for color in palette[:3]]
        sorted_hues = sorted(hues)

        # Calculate gaps between consecutive hues
        gaps = []
        for i in range(len(sorted_hues)):
            next_i = (i + 1) % len(sorted_hues)
            gap = sorted_hues[next_i] - sorted_hues[i]
            if gap < 0:
                gap += 1
            gaps.append(gap)

        # Each gap should be close to 1/3 (120 degrees)
        for gap in gaps:
            assert abs(gap - 1 / 3) < 0.2

    def test_analogous_palette(self):
        """Test analogous palette generation."""
        palette = generate_analogous_palette(0.5, 0.8, 0.5)  # Cyan base

        assert len(palette) == 5
        assert all(color.startswith("#") for color in palette)

        # All hues should be close to each other
        hues = [hex_to_hsl(color)[0] for color in palette]
        hue_spread = max(hues) - min(hues)

        # Handle wrap-around case
        if hue_spread > 0.5:
            hue_spread = 1 - hue_spread

        # Analogous colors should be within ~60 degrees (1/6 of circle)
        assert hue_spread < 0.2

    def test_tetradic_palette(self):
        """Test tetradic palette generation."""
        palette = generate_tetradic_palette(0.0, 0.8, 0.5)

        assert len(palette) == 5
        assert all(color.startswith("#") for color in palette)

        # First four colors should be roughly 90 degrees apart
        hues = [hex_to_hsl(color)[0] for color in palette[:4]]
        sorted_hues = sorted(hues)

        gaps = []
        for i in range(len(sorted_hues)):
            next_i = (i + 1) % len(sorted_hues)
            gap = sorted_hues[next_i] - sorted_hues[i]
            if gap < 0:
                gap += 1
            gaps.append(gap)

        # Each gap should be close to 1/4 (90 degrees)
        for gap in gaps:
            assert abs(gap - 0.25) < 0.2

    def test_monochromatic_palette(self):
        """Test monochromatic palette generation."""
        palette = generate_monochromatic_palette(0.3, 0.8, 0.5)

        assert len(palette) == 5
        assert all(color.startswith("#") for color in palette)

        # All colors should have the same hue
        hues = [hex_to_hsl(color)[0] for color in palette]
        base_hue = hues[0]

        for hue in hues:
            assert abs(hue - base_hue) < 0.01

    def test_split_complementary_palette(self):
        """Test split-complementary palette generation."""
        palette = generate_split_complementary_palette(0.0, 0.8, 0.5)  # Red base

        assert len(palette) == 5
        assert all(color.startswith("#") for color in palette)

        # Should have base color and two colors near its complement
        base_h = hex_to_hsl(palette[0])[0]
        comp_h1 = hex_to_hsl(palette[1])[0]
        comp_h2 = hex_to_hsl(palette[2])[0]

        # Complement should be around 0.5 (180 degrees) from base
        expected_comp = normalize_hue(base_h + 0.5)

        # Both complement colors should be close to the expected complement
        diff1 = abs(comp_h1 - expected_comp)
        if diff1 > 0.5:
            diff1 = 1 - diff1

        diff2 = abs(comp_h2 - expected_comp)
        if diff2 > 0.5:
            diff2 = 1 - diff2

        assert diff1 < 0.2
        assert diff2 < 0.2


class TestRandomPaletteGeneration:
    """Test random palette generation with various options."""

    def test_random_palette_basic(self):
        """Test basic random palette generation."""
        palette = generate_random_harmonious_palette()

        assert len(palette) == 5
        assert all(color.startswith("#") for color in palette)
        assert all(len(color) == 7 for color in palette)

    def test_random_palette_with_harmony_type(self):
        """Test random palette with specific harmony type."""
        for harmony_type in HARMONY_GENERATORS.keys():
            palette = generate_random_harmonious_palette(harmony_type=harmony_type)

            assert len(palette) == 5
            assert all(color.startswith("#") for color in palette)

    def test_random_palette_with_locked_colors(self):
        """Test random palette generation with locked colors."""
        locked_colors = ["#ff0000", "#00ff00"]
        palette = generate_random_harmonious_palette(locked_colors=locked_colors)

        assert len(palette) == 5
        assert palette[0] == "#ff0000"
        assert palette[1] == "#00ff00"
        assert all(color.startswith("#") for color in palette)

    def test_random_palette_deterministic_with_locked(self):
        """Test that locked colors are preserved."""
        locked_colors = ["#123456"]

        # Generate multiple palettes
        palettes = [
            generate_random_harmonious_palette(locked_colors=locked_colors)
            for _ in range(5)
        ]

        # First color should always be the locked color
        for palette in palettes:
            assert palette[0] == "#123456"

    def test_invalid_harmony_type(self):
        """Test handling of invalid harmony type."""
        palette = generate_random_harmonious_palette(harmony_type="invalid_type")

        # Should still generate a valid palette
        assert len(palette) == 5
        assert all(color.startswith("#") for color in palette)


class TestHarmonyValidation:
    """Test color harmony validation."""

    def test_complementary_validation(self):
        """Test validation of complementary harmony."""
        # Create a perfect complementary pair
        colors = ["#ff0000", "#00ffff"]  # Red and cyan (complementary)
        result = validate_color_harmony(colors, "complementary")

        assert result["valid"] is True
        assert result["harmony_type"] == "complementary"
        assert result["confidence"] > 0.8

    def test_triadic_validation(self):
        """Test validation of triadic harmony."""
        # Create colors roughly 120 degrees apart
        colors = ["#ff0000", "#00ff00", "#0000ff"]  # Red, green, blue
        result = validate_color_harmony(colors, "triadic")

        assert result["valid"] is True
        assert result["harmony_type"] == "triadic"
        assert "hue_gaps" in result["details"]

    def test_analogous_validation(self):
        """Test validation of analogous harmony."""
        # Create colors close to each other
        colors = ["#ff0000", "#ff3300", "#ff6600"]  # Red to orange
        result = validate_color_harmony(colors, "analogous")

        assert result["valid"] is True
        assert result["harmony_type"] == "analogous"
        assert "hue_spread" in result["details"]

    def test_validation_insufficient_colors(self):
        """Test validation with insufficient colors."""
        colors = ["#ff0000"]
        result = validate_color_harmony(colors, "complementary")

        assert result["valid"] is False
        assert "Need at least 2 colors" in result["reason"]

    def test_validation_confidence_scoring(self):
        """Test that confidence scoring works properly."""
        # Perfect complementary colors
        perfect_comp = ["#ff0000", "#00ffff"]
        result1 = validate_color_harmony(perfect_comp, "complementary")

        # Imperfect complementary colors
        imperfect_comp = [
            "#ff0000",
            "#00ff00",
        ]  # Red and green (not quite complementary)
        result2 = validate_color_harmony(imperfect_comp, "complementary")

        # Perfect should have higher confidence
        assert result1["confidence"] > result2["confidence"]


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_extreme_hsl_values(self):
        """Test with extreme HSL values."""
        # Test with extreme values
        palette = generate_complementary_palette(0.0, 1.0, 0.0)  # Pure black base
        assert len(palette) == 5

        palette = generate_complementary_palette(0.0, 0.0, 1.0)  # Pure white base
        assert len(palette) == 5

    def test_many_locked_colors(self):
        """Test with many locked colors."""
        locked_colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff"]
        palette = generate_random_harmonious_palette(locked_colors=locked_colors)

        assert len(palette) == 5
        # All colors should be the locked colors
        for i, locked in enumerate(locked_colors):
            assert palette[i] == locked

    def test_empty_locked_colors(self):
        """Test with empty locked colors list."""
        palette = generate_random_harmonious_palette(locked_colors=[])

        assert len(palette) == 5
        assert all(color.startswith("#") for color in palette)

    def test_color_format_consistency(self):
        """Test that all generated colors follow consistent format."""
        for harmony_type in HARMONY_GENERATORS.keys():
            palette = generate_random_harmonious_palette(harmony_type=harmony_type)

            for color in palette:
                # Should be valid hex format
                assert color.startswith("#")
                assert len(color) == 7
                # Should be valid hex digits
                hex_part = color[1:]
                assert all(c in "0123456789abcdef" for c in hex_part.lower())


if __name__ == "__main__":
    pytest.main([__file__])
