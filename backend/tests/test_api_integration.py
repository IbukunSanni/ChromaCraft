"""
Integration tests for the random palette generation API endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


class TestRandomPaletteAPI:
    """Test the /generate/random API endpoint."""

    def test_basic_random_generation(self):
        """Test basic random palette generation."""
        response = client.post("/generate/random", json={})

        assert response.status_code == 200
        data = response.json()

        assert "colors" in data
        assert "names" in data
        assert "harmony_info" in data

        assert len(data["colors"]) == 5
        assert len(data["names"]) == 5

        # Check color format
        for color in data["colors"]:
            assert color.startswith("#")
            assert len(color) == 7

        # Check harmony info structure
        harmony_info = data["harmony_info"]
        assert "valid" in harmony_info
        assert "harmony_type" in harmony_info
        assert "confidence" in harmony_info

    def test_specific_harmony_type(self):
        """Test generation with specific harmony type."""
        harmony_types = [
            "complementary",
            "triadic",
            "analogous",
            "tetradic",
            "monochromatic",
            "split_complementary",
        ]

        for harmony_type in harmony_types:
            response = client.post(
                "/generate/random", json={"harmony_type": harmony_type}
            )

            assert response.status_code == 200
            data = response.json()

            assert len(data["colors"]) == 5
            assert len(data["names"]) == 5
            assert data["harmony_info"]["harmony_type"] == harmony_type

    def test_locked_colors(self):
        """Test generation with locked colors."""
        locked_colors = ["#ff0000", "#00ff00"]

        response = client.post(
            "/generate/random", json={"locked_colors": locked_colors}
        )

        assert response.status_code == 200
        data = response.json()

        assert len(data["colors"]) == 5
        assert data["colors"][0] == "#ff0000"
        assert data["colors"][1] == "#00ff00"

    def test_locked_colors_with_harmony(self):
        """Test generation with locked colors and specific harmony."""
        response = client.post(
            "/generate/random",
            json={"locked_colors": ["#ff0000"], "harmony_type": "complementary"},
        )

        assert response.status_code == 200
        data = response.json()

        assert len(data["colors"]) == 5
        assert data["colors"][0] == "#ff0000"
        assert data["harmony_info"]["harmony_type"] == "complementary"

    def test_invalid_harmony_type(self):
        """Test with invalid harmony type (should still work)."""
        response = client.post(
            "/generate/random", json={"harmony_type": "invalid_type"}
        )

        assert response.status_code == 200
        data = response.json()

        assert len(data["colors"]) == 5
        assert len(data["names"]) == 5

    def test_empty_request(self):
        """Test with completely empty request."""
        response = client.post("/generate/random", json={})

        assert response.status_code == 200
        data = response.json()

        assert len(data["colors"]) == 5
        assert len(data["names"]) == 5

    def test_many_locked_colors(self):
        """Test with maximum locked colors."""
        locked_colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff"]

        response = client.post(
            "/generate/random", json={"locked_colors": locked_colors}
        )

        assert response.status_code == 200
        data = response.json()

        assert len(data["colors"]) == 5
        for i, locked_color in enumerate(locked_colors):
            assert data["colors"][i] == locked_color

    def test_response_structure(self):
        """Test that response follows the expected structure."""
        response = client.post("/generate/random", json={"harmony_type": "triadic"})

        assert response.status_code == 200
        data = response.json()

        # Check main structure
        assert isinstance(data["colors"], list)
        assert isinstance(data["names"], list)
        assert isinstance(data["harmony_info"], dict)

        # Check harmony info structure
        harmony_info = data["harmony_info"]
        assert isinstance(harmony_info["valid"], bool)
        assert isinstance(harmony_info["harmony_type"], str)
        assert isinstance(harmony_info["confidence"], (int, float))
        assert "details" in harmony_info

    def test_color_name_matching(self):
        """Test that color names are properly matched."""
        response = client.post("/generate/random", json={})

        assert response.status_code == 200
        data = response.json()

        # Each color should have a corresponding name
        assert len(data["colors"]) == len(data["names"])

        # Names should be strings
        for name in data["names"]:
            assert isinstance(name, str)
            assert len(name) > 0


if __name__ == "__main__":
    pytest.main([__file__])
