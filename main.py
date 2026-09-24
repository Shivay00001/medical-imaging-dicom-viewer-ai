#!/usr/bin/env python3
"""Top-level entry point — runs the REAL DICOM viewer API (src/main.py).

The previous top-level main.py was an unrelated random-/predict stub; it has
been replaced with this thin launcher for the real flow:
    DICOM upload -> pydicom parsing -> U-Net segmentation -> /analyze, /health
"""
import uvicorn

from src.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
