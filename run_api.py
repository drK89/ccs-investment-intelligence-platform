"""Convenience launcher for the FastAPI service."""

from __future__ import annotations

import sys
from pathlib import Path

import uvicorn

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))


if __name__ == "__main__":
    uvicorn.run("ccs_platform.api:app", host="0.0.0.0", port=8000, reload=True)

