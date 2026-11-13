"""
Baseline tests for application wiring: startup without AI configuration,
CORS origins, image extraction, and PNG export request format.
"""

from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from PIL import Image

import utils.openai_palette_generator as openai_palette_generator
from config import Config
from main import app
from mycolors.xkcd_colors import xkcd_colors


client = TestClient(app)


def _png_bytes() -> bytes:
    """Build a small four-color PNG in memory."""
    image = Image.new("RGB", (40, 40), "#ff0000")
    image.paste((0, 128, 255), (20, 0, 40, 20))
    image.paste((0, 200, 0), (0, 20, 20, 40))
    image.paste((250, 220, 0), (20, 20, 40, 40))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


class TestStartup:
    def test_health_check(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_color_names_loaded(self):
        # The XKCD survey dataset has 954 named colors.
        assert len(xkcd_colors) == 954
        assert all(value.startswith("#") for value in xkcd_colors.values())

    def test_concept_generation_without_api_key_returns_503(self, monkeypatch):
        monkeypatch.setattr(Config, "OPENAI_API_KEY", None)
        monkeypatch.setattr(openai_palette_generator, "_openai_generator", None)

        response = client.post("/generate/concept", json={"concept": "sunset"})

        assert response.status_code == 503
        assert "OPENAI_API_KEY" in response.json()["detail"]


class TestCors:
    @pytest.mark.parametrize(
        "origin",
        [
            "http://localhost:3000",
            "https://color-palette-extractor.vercel.app",
            "https://color-palette-extractor-74qrycbse-ibukunsanni-projects.vercel.app",
        ],
    )
    def test_allowed_origins(self, origin):
        response = client.options(
            "/generate/random",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
            },
        )
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == origin

    @pytest.mark.parametrize(
        "origin",
        ["https://evil.vercel.app", "https://color-palette-extractor.vercel.app.evil.com"],
    )
    def test_rejected_origins(self, origin):
        response = client.options(
            "/generate/random",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
            },
        )
        assert response.headers.get("access-control-allow-origin") is None


class TestImageExtraction:
    def test_extract_colors_from_png(self):
        response = client.post(
            "/extract-colors",
            files={"file": ("palette.png", _png_bytes(), "image/png")},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["colors"]) >= 1
        assert len(data["names"]) == len(data["colors"])
        for color in data["colors"]:
            assert color.startswith("#") and len(color) == 7

    def test_extract_colors_rejects_non_image(self):
        response = client.post(
            "/extract-colors",
            files={"file": ("notes.txt", b"not an image", "text/plain")},
        )

        assert response.status_code == 400


class TestPngExport:
    def test_export_png_with_repeated_color_fields(self):
        # The frontend sends one "colors" form field per color.
        response = client.post(
            "/export-png",
            data={"colors": ["#ff0000", "#00ff00", "#0000ff"]},
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        image = Image.open(BytesIO(response.content))
        assert image.size == (300, 100)
