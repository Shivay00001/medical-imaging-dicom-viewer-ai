"""Medical Imaging DICOM viewer API — real flow.

Upload a .dcm file -> real metadata + pixel extraction via pydicom
(src/imaging/handler.py) -> real U-Net forward pass when torch is installed
(no more mocked "AI analysis completed" string). Without torch, the endpoint
honestly reports segmentation as unavailable instead of faking it.

Optional: set SEGMENTATION_MODEL_PATH to load trained U-Net weights.
The bundled model ships UNTRAINED — its mask statistics are experimental
and must not be used for diagnosis.
"""
import os

from fastapi import FastAPI, UploadFile, File, HTTPException

from src.imaging.handler import DICOMHandler

try:
    import torch
    from src.models.segmentation import load_segmentation_model
    TORCH_AVAILABLE = True
except ImportError:
    torch = None
    load_segmentation_model = None
    TORCH_AVAILABLE = False

app = FastAPI(title="Medical Imaging AI API")

_model = None


def get_model():
    """Lazily load the U-Net (real inference, untrained weights unless
    SEGMENTATION_MODEL_PATH points at trained weights)."""
    global _model
    if _model is None:
        if not TORCH_AVAILABLE:
            raise RuntimeError("torch is not installed; segmentation unavailable")
        _model = load_segmentation_model(os.environ.get("SEGMENTATION_MODEL_PATH") or None)
    return _model


@app.post("/analyze")
async def analyze_dicom(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        metadata = DICOMHandler.read_metadata(temp_path)
        pixels = DICOMHandler.get_pixel_data(temp_path)  # normalized uint8 HxW

        analysis = {
            "pixel_shape": list(pixels.shape),
            "pixel_mean": round(float(pixels.mean()), 2),
            "pixel_std": round(float(pixels.std()), 2),
        }

        if TORCH_AVAILABLE:
            model = get_model()
            with torch.no_grad():
                tensor = torch.from_numpy(pixels.astype("float32") / 255.0).unsqueeze(0).unsqueeze(0)
                mask = model(tensor).squeeze().numpy()
            analysis["segmentation"] = {
                "mask_mean": round(float(mask.mean()), 4),
                "mask_max": round(float(mask.max()), 4),
                "anomaly_score": round(float((mask > 0.5).mean()), 4),
                "note": ("Experimental output from an UNTRAINED U-Net. "
                         "Set SEGMENTATION_MODEL_PATH to trained weights for real use. "
                         "Not for diagnosis."),
            }
        else:
            analysis["segmentation"] = {
                "status": "unavailable",
                "reason": "torch is not installed; install torch to enable U-Net inference",
            }

        return {"status": "success", "metadata": metadata, "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.get("/health")
async def health():
    return {"status": "ok", "torch_available": TORCH_AVAILABLE}
