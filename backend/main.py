"""
ChromaCraft Backend - AI-Powered Color Palette Generation API

This FastAPI application provides endpoints for:
- Random harmonious color palette generation
- AI-powered concept-based palette creation using OpenAI
- Image color extraction and analysis
- Color palette adjustment and export

Author: ChromaCraft Team
Version: 1.0.0
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import route modules
from routes import health, palettes, colors

# Create FastAPI app instance
app = FastAPI(
    title="ChromaCraft API",
    description="AI-Powered Color Palette Generation & Extraction API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
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

# Include route modules
app.include_router(health.router)
app.include_router(palettes.router)
app.include_router(colors.router)


# Application lifecycle events
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    print("🚀 ChromaCraft API starting up...")
    print("📚 Documentation available at: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    print("⏹️  ChromaCraft API shutting down...")