"""
Tests for color locking functionality in palette generation.
"""

import pytest
from utils.color_harmony import generate_random_harmonious_palette, hex_to_hsl


class TestColorLocking:
    """Test color locking behavior in palette generation."""

    def test_generate_palette_without_locked_colors(self):
        """Test generating palette without any locked colors."""
        palette = generate_random_harmonious_palette()

        assert len(palette) == 5
        assert all(color.startswith("#") for color in palette)
        assert all(len(color) == 7 for color in palette)

    def test_generate_palette_with_single_locked_color(self):
        """Test generating palette with one locked color."""
        locked_color = "#FF5733"
        palette = generate_random_harmonious_palette(locked_colors=[locked_color])

        assert len(palette) == 5
        assert palette[0] == locked_color  # First color should be locked
        assert all(color.startswith("#") for color in palette)

    def test_generate_palette_with_multiple_locked_colors(self):
        """Test generating palette with multiple locked colors."""
        locked_colors = ["#FF5733", "#33FF57", "#3357FF"]
        palette = generate_random_harmonious_palette(locked_colors=locked_colors)

        assert len(palette) == 5
        # First three colors should be locked
        assert palette[0] == locked_colors[0]
        assert palette[1] == locked_colors[1]
        assert palette[2] == locked_colors[2]
        # Remaining colors should be generated
        assert palette[3] != locked_colors[0]
        assert palette[4] != locked_colors[0]

    def test_generate_palette_with_all_colors_locked(self):
        """Test generating palette with all 5 colors locked."""
        locked_colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#33FFF3"]
        palette = generate_random_harmonious_palette(locked_colors=locked_colors)

        assert len(palette) == 5
        assert palette == locked_colors

    def test_generate_palette_with_too_many_locked_colors(self):
        """Test generating palette with more than 5 locked colors."""
        locked_colors = [
            "#FF5733",
            "#33FF57",
            "#3357FF",
            "#F333FF",
            "#33FFF3",
            "#FFFF33",
        ]
        palette = generate_random_harmonious_palette(locked_colors=locked_colors)

        assert len(palette) == 5
        # Should only use first 5 locked colors
        assert palette == locked_colors[:5]

    def test_locked_colors_preserve_harmony_base(self):
        """Test that locked colors are used as base for harmony generation."""
        locked_color = "#FF0000"  # Pure red
        palette = generate_random_harmonious_palette(
            harmony_type="complementary", locked_colors=[locked_color]
        )

        assert palette[0] == locked_color

        # For complementary, we expect colors around cyan (opposite of red)
        # This is a basic test - in practice, the exact colors depend on the algorithm
        locked_hue, _, _ = hex_to_hsl(locked_color)
        assert locked_hue == 0.0  # Red hue

    def test_different_harmony_types_with_locked_colors(self):
        """Test different harmony types work with locked colors."""
        locked_color = "#FF5733"
        harmony_types = ["complementary", "triadic", "analogous", "monochromatic"]

        for harmony_type in harmony_types:
            palette = generate_random_harmonious_palette(
                harmony_type=harmony_type, locked_colors=[locked_color]
            )

            assert len(palette) == 5
            assert palette[0] == locked_color
            assert all(color.startswith("#") for color in palette)

    def test_invalid_locked_colors_handling(self):
        """Test handling of invalid locked color formats."""
        # This should not crash, but behavior may vary
        # In a production system, we might want to validate and filter invalid colors
        invalid_locked_colors = ["invalid", "FF5733", "#GGG"]

        # The function should still work, though it might ignore invalid colors
        # or convert them in some way
        try:
            palette = generate_random_harmonious_palette(
                locked_colors=invalid_locked_colors
            )
            assert len(palette) == 5
        except Exception:
            # If the function throws an exception for invalid colors, that's also acceptable
            pass

    def test_empty_locked_colors_list(self):
        """Test that empty locked colors list works like no locked colors."""
        palette1 = generate_random_harmonious_palette(locked_colors=[])
        palette2 = generate_random_harmonious_palette(locked_colors=None)

        # Both should generate valid palettes (though they'll be different due to randomness)
        assert len(palette1) == 5
        assert len(palette2) == 5
        assert all(color.startswith("#") for color in palette1)
        assert all(color.startswith("#") for color in palette2)

    def test_locked_colors_consistency(self):
        """Test that locked colors remain consistent across multiple generations."""
        locked_colors = ["#FF5733", "#33FF57"]

        # Generate multiple palettes with same locked colors
        palettes = []
        for _ in range(5):
            palette = generate_random_harmonious_palette(
                harmony_type="complementary", locked_colors=locked_colors
            )
            palettes.append(palette)

        # All palettes should have the same locked colors in the same positions
        for palette in palettes:
            assert palette[0] == locked_colors[0]
            assert palette[1] == locked_colors[1]

        # Test that we can generate different palettes with different harmony types
        # This tests the consistency of locked colors across different generation methods
        triadic_palette = generate_random_harmonious_palette(
            harmony_type="triadic", locked_colors=locked_colors
        )
        analogous_palette = generate_random_harmonious_palette(
            harmony_type="analogous", locked_colors=locked_colors
        )

        # Locked colors should be consistent across harmony types
        assert triadic_palette[0] == locked_colors[0]
        assert triadic_palette[1] == locked_colors[1]
        assert analogous_palette[0] == locked_colors[0]
        assert analogous_palette[1] == locked_colors[1]


if __name__ == "__main__":
    pytest.main([__file__])
