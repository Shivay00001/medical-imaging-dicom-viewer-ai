#!/usr/bin/env python3
"""Regenerate tests/sample.dcm — a real (synthetic) DICOM for verification."""
import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
from pathlib import Path

OUT = Path(__file__).parent / "sample.dcm"

pixels = (np.random.default_rng(42).normal(1000, 200, (64, 64))).astype(np.int16)
yy, xx = np.ogrid[:64, :64]
pixels[((yy - 32) ** 2 + (xx - 32) ** 2) < 100] = 2500  # bright blob

file_meta = Dataset()
file_meta.MediaStorageSOPClassUID = generate_uid()
file_meta.MediaStorageSOPInstanceUID = generate_uid()
file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

ds = FileDataset(str(OUT), {}, file_meta=file_meta, preamble=b"\0" * 128)
ds.PatientName = "Test^Patient"
ds.PatientID = "TEST123"
ds.Modality = "CT"
ds.StudyDescription = "Wave-1 verification scan"
ds.PixelSpacing = [0.5, 0.5]
ds.Rows, ds.Columns = 64, 64
ds.BitsAllocated, ds.BitsStored, ds.HighBit = 16, 16, 15
ds.PixelRepresentation = 1
ds.SamplesPerPixel = 1
ds.PhotometricInterpretation = "MONOCHROME2"
ds.PixelData = pixels.tobytes()
ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
ds.save_as(str(OUT))
print(f"wrote {OUT}")
