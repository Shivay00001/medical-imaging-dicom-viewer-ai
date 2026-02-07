from fastapi import FastAPI, UploadFile, File, HTTPException
from src.imaging.handler import DICOMHandler
from src.models.segmentation import load_segmentation_model
import torch
from torchvision import transforms
import os

app = FastAPI(title="Medical Imaging AI API")
model = load_segmentation_model()

@app.post("/analyze")
async def analyze_dicom(file: UploadFile = File(...)):
    # Save temp file
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
        
    try:
        # Extract metadata
        metadata = DICOMHandler.read_metadata(temp_path)
        
        # Ingest for AI
        pixels = DICOMHandler.get_pixel_data(temp_path)
        # (Preprocessing and Inference logic would go here)
        
        return {
            "status": "success",
            "metadata": metadata,
            "analysis": {
                "anomalies_detected": False,
                "message": "AI analysis completed (mock)"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/health")
async def health():
    return {"status": "ok"}
