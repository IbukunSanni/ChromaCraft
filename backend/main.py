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

import sys
from contextlib import asynccontextmanager

# Log lines contain emoji. On Windows, redirected stdout/stderr (e.g. under
# `pnpm run dev`/concurrently) default to cp1252 and would raise
# UnicodeEncodeError, failing startup and requests. Escape instead of crashing.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="backslashreplace")
    except (AttributeError, ValueError):
        pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Config

# Import route modules
from routes import health, palettes, colors


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown hooks."""
    print("🚀 ChromaCraft API starting up...")
    print("📚 Documentation available at: /docs")
    if not Config.OPENAI_API_KEY:
        print("⚠️  OPENAI_API_KEY is not set: /generate/concept will return 503")
    yield
    print("⏹️  ChromaCraft API shutting down...")


# Create FastAPI app instance
app = FastAPI(
    title="ChromaCraft API",
    description="AI-Powered Color Palette Generation & Extraction API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware configuration (origins are configured via environment;
# see Config.ALLOWED_ORIGINS and Config.ALLOWED_ORIGIN_REGEX)
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_origin_regex=Config.ALLOWED_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(health.router)
app.include_router(palettes.router)
app.include_router(colors.router)