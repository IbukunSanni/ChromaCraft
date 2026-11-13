#!/usr/bin/env python3
"""
Production entry point for the ChromaCraft API (used by Railway).

Binds to all interfaces on the port in $PORT, which Railway injects and routes
its public domain to. Reading the port in Python avoids relying on shell
expansion of "$PORT" in the start command. Falls back to 8000 locally.
"""

import os

import uvicorn


def main() -> None:
    port = int(os.environ.get("PORT", "8000"))
    print(f"ChromaCraft API listening on 0.0.0.0:{port}", flush=True)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    main()
