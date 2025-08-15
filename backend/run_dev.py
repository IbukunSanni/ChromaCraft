#!/usr/bin/env python3
"""
Development server runner for the FastAPI backend.
Run this instead of uvicorn directly to ensure proper CORS setup.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,  # Use 8000 for local development
        reload=True,  # Auto-reload on code changes
        log_level="info",
    )
