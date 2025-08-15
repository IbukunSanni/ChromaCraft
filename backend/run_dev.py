#!/usr/bin/env python3
"""
Development server runner for the FastAPI backend.
Run this instead of uvicorn directly to ensure proper CORS setup.
"""

import uvicorn
import sys
import os


def check_venv():
    """Check if we're running in a virtual environment"""
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("✅ Virtual environment is active")
        return True
    else:
        print("❌ Virtual environment not detected!")
        print("Please activate your virtual environment first:")
        print("  Windows: .\\venv\\Scripts\\activate")
        print("  Linux/Mac: source venv/bin/activate")
        return False


if __name__ == "__main__":
    if not check_venv():
        sys.exit(1)

    print("🚀 Starting FastAPI development server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,  # Use 8000 for local development
        reload=True,  # Auto-reload on code changes
        log_level="info",
    )
