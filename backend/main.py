from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from utils.color_extractor import extract_colors
from utils.png_exporter import generate_png_swatch
from utils.find_closest_color_name import find_closest_color_name
from utils.mood_adjuster import get_adjustment_weights, adjust_palette_by_mood
from utils.openai_palette_generator import openai_generator
from utils.color_harmony import (
    generate_random_harmonious_palette,
    validate_color_harmony,
)
import time
import io
import psutil, os  # ⬅️ NEW: for memory tracking
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from mycolors.xkcd_colors import xkcd_colors


app = FastAPI()


# Pydantic models for request/response validation
class RandomPaletteRequest(BaseModel):
    locked_colors: Optional[List[str]] = None
    harmony_type: Optional[str] = None


class ConceptPaletteRequest(BaseModel):
    concept: str
    color_count: Optional[int] = 5


class PaletteResponse(BaseModel):
    colors: List[str]
    names: List[str]
    harmony_info: dict


# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",  # Alternative localhost
        "https://color-palette-extractor.vercel.app",  # Production frontend
        "https://*.vercel.app",  # Any Vercel deployment
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "✅ FastAPI backend is running!"}


@app.options("/{path:path}")
def options_handler(path: str):
    """Handle CORS preflight requests"""
    return {"message": "OK"}


@app.post("/")
def post_root():
    return {"message": "✅ POST received! FastAPI is working."}


@app.post("/generate/random")
async def generate_random_palette(request: RandomPaletteRequest):
    """Generate a random harmonious color palette with support for locked colors."""
    try:
        print(f"🎨 Generating random palette with harmony: {request.harmony_type}")
        print(f"🔒 Locked colors: {request.locked_colors}")

        # Generate the palette
        colors = generate_random_harmonious_palette(
            harmony_type=request.harmony_type, locked_colors=request.locked_colors or []
        )

        # Get color names
        names = [find_closest_color_name(color, xkcd_colors) for color in colors]

        # Validate harmony
        harmony_type = request.harmony_type or "random"
        harmony_info = validate_color_harmony(colors, harmony_type)

        # Add locked colors info to harmony_info
        if request.locked_colors:
            harmony_info["locked_colors_count"] = len(request.locked_colors)
            harmony_info["locked_colors"] = request.locked_colors

        print(f"✅ Generated palette: {colors}")
        print(f"📊 Harmony validation: {harmony_info}")

        return PaletteResponse(colors=colors, names=names, harmony_info=harmony_info)

    except Exception as e:
        print(f"❌ Error generating random palette: {e}")
        raise HTTPException(
            status_code=500, detail=f"Random palette generation failed: {str(e)}"
        )


@app.post("/extract-colors")
async def extract_colors_endpoint(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Normalize mode to RGB if needed
        if image.mode in ("RGBA", "P", "L"):
            image = image.convert("RGB")
        image = image.resize((100, 100))  # optional

        # Step 3: Save resized image into an in-memory file-like object
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)  # Go back to the start of the buffer

        # Step 4: Extract colors
        colors = extract_colors(buffer)
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image file.")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Image processing failed: {str(e)}"
        )

    names = [find_closest_color_name(color, xkcd_colors) for color in colors]
    return {"colors": colors, "names": names}


# 🧠 Adjust palette by mood
@app.post("/adjust-mood")
async def adjust_mood_endpoint(
    mood: str = Form(...), base_colors: list[str] = Form(...)
):
    start = time.time()
    try:
        print(f"🎯 Adjusting mood: '{mood}' for {len(base_colors)} colors")

        weights = await get_adjustment_weights(mood)
        palette = adjust_palette_by_mood(base_colors, weights)
        names = [find_closest_color_name(color, xkcd_colors) for color in palette]

        print(f"✅ Done in {time.time() - start:.2f}s")
        print_mem("after /adjust-mood")

        return {"adjusted_colors": palette, "names": names}
    except Exception as e:
        print(f"❌ Error in /adjust-mood: {e}")
        raise HTTPException(status_code=500, detail="Mood adjustment failed.")


@app.post("/export-png")
async def export_png(colors: list[str] = Form(...)):
    image = generate_png_swatch(colors)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")


# 🤖 Generate palette from concept using OpenAI
@app.post("/generate/concept")
async def generate_palette_from_concept(request: ConceptPaletteRequest):
    """Generate a color palette from a concept description using OpenAI."""
    start = time.time()
    try:
        print(f"🤖 Generating palette for concept: '{request.concept}'")
        print(f"📊 Color count: {request.color_count}")
        
        # Generate palette using OpenAI
        result = await openai_generator.generate_palette_from_concept(
            concept=request.concept,
            color_count=request.color_count
        )
        
        # Add timestamp to metadata
        result["metadata"]["timestamp"] = time.time()
        
        # Create response in the same format as other endpoints
        colors = result["colors"]
        names = result["names"]
        
        # Additional harmony info from OpenAI
        harmony_info = {
            "type": result.get("harmony_type", "ai_generated"),
            "mood": result.get("mood", "generated"),
            "description": result.get("description", ""),
            "source": "openai",
            "model": result["metadata"]["model"]
        }
        
        print(f"✅ Generated {len(colors)} colors in {time.time() - start:.2f}s")
        print(f"🎨 Colors: {colors}")
        print(f"💭 Original concept: {result.get('concept', 'N/A')}")
        print_mem("after /generate/concept")
        
        return PaletteResponse(colors=colors, names=names, harmony_info=harmony_info)
        
    except Exception as e:
        print(f"❌ Error in /generate/concept: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Concept-based palette generation failed: {str(e)}"
        )


# ✅ NEW: Memory usage monitor
@app.get("/mem")
def get_memory_usage():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)
    return {"memory_mb": round(mem, 2)}


# ✅ Memory log function for print-based monitoring
def print_mem(tag=""):
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)
    print(f"📦 {tag} - Memory: {mem:.2f} MB")
