# Medical Imaging DICOM Viewer AI

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C.svg)](https://pytorch.org/)
[![pydicom](https://img.shields.io/badge/pydicom-2.4-green.svg)](https://pydicom.github.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **production-grade medical imaging platform** for viewing and analyzing DICOM (Digital Imaging and Communications in Medicine) files. This repository integrates standard medical imaging protocols with advanced deep learning models for automated organ segmentation and anomaly detection.

## 🚀 Features

- **DICOM Parsing**: Full support for reading and extracting metadata from DICOM files and series.
- **AI Segmentation**: Integrated U-Net architecture for high-precision segmentation of medical images.
- **FastAPI Interface**: RESTful API for asynchronous image processing and model inference.
- **Batch Analysis**: Efficiently process entire DICOM series (CT/MRI) in a single workflow.
- **Durable IO**: Optimized handling of large medical imaging datasets.
- **Containerized**: Standardized Docker environment for deployment in clinical and research settings.

## 📁 Project Structure

```
medical-imaging-dicom-viewer-ai/
├── src/
│   ├── api/          # API route handlers
│   ├── imaging/      # DICOM and image processing logic
│   ├── models/       # PyTorch segmentation models
│   └── main.py       # Application entrypoint
├── tests/            # Unit and clinical validation tests
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🛠️ Quick Start

```bash
# Clone
git clone https://github.com/Shivay00001/medical-imaging-dicom-viewer-ai.git

# Install
pip install -r requirements.txt

# Run Service
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## 📄 License

MIT License
