from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from utils.color_extractor import extract_colors
from utils.png_exporter import generate_png_swatch
from utils.find_closest_color_name import find_closest_color_name
from utils.mood_adjuster import get_adjustment_weights, adjust_palette_by_mood
import time
import io
import psutil, os  # ⬅️ NEW: for memory tracking
from PIL import Image, UnidentifiedImageError
from mycolors.xkcd_colors import xkcd_colors


app = FastAPI()

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
