import pydicom
import numpy as np
from PIL import Image
import io

class DICOMHandler:
    @staticmethod
    def read_metadata(filepath):
        """Reads and returns DICOM metadata as a dictionary."""
        ds = pydicom.dcmread(filepath)
        return {
            "patient_name": str(ds.PatientName),
            "patient_id": ds.PatientID,
            "modality": ds.Modality,
            "study_description": getattr(ds, "StudyDescription", "N/A"),
            "pixel_spacing": [float(v) for v in ds.PixelSpacing] if hasattr(ds, "PixelSpacing") else []
        }

    @staticmethod
    def get_pixel_data(filepath):
        """Extracts and normalizes pixel data from a DICOM file."""
        ds = pydicom.dcmread(filepath)
        pixels = ds.pixel_array.astype(float)
        # Normalize to 0-255
        pixels = (np.maximum(pixels, 0) / pixels.max()) * 255.0
        return pixels.astype(np.uint8)

    @staticmethod
    def pixels_to_image(pixels):
        """Converts pixel array to PIL Image."""
        return Image.fromarray(pixels)
