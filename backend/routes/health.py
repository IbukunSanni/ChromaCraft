"""
Health check and system monitoring routes.
"""

from fastapi import APIRouter

# Optional memory tracking (only import if needed)
try:
    import psutil
    import os
    MEMORY_TRACKING_AVAILABLE = True
except ImportError:
    MEMORY_TRACKING_AVAILABLE = False

router = APIRouter(prefix="", tags=["health"])


@router.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "✅ FastAPI backend is running!"}


@router.post("/")
def post_root():
    """POST health check endpoint."""
    return {"message": "✅ POST received! FastAPI is working."}


@router.options("/{path:path}", tags=["cors"])
def options_handler(path: str):
    """Handle CORS preflight requests."""
    return {"message": "OK"}


@router.get("/mem")
def get_memory_usage():
    """Get current memory usage if psutil is available."""
    if not MEMORY_TRACKING_AVAILABLE:
        return {"error": "Memory tracking not available (psutil not installed)"}
    
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)
    return {"memory_mb": round(mem, 2)}


def print_mem(tag=""):
    """Print memory usage if available, otherwise skip silently."""
    if not MEMORY_TRACKING_AVAILABLE:
        return  # Skip silently if not available
    
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)
    print(f"📦 {tag} - Memory: {mem:.2f} MB")