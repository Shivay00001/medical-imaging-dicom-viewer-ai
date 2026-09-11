# Medical Imaging Dicom Viewer Ai

An enterprise-grade solution engineered for high performance.

![Language](https://img.shields.io/badge/Language-Python-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-Custom%20(VisionQuantech)-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-ee4c2c)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)

## 🚀 Overview

Welcome to the **Medical Imaging Dicom Viewer Ai** repository. This project is built to deliver a robust and scalable solution tailored to modern development standards.

Specifically, this is a **FastAPI-based microservice for ingesting, parsing, and analyzing DICOM (`.dcm`) medical imaging files**. It combines:

- **DICOM metadata extraction** and pixel-data normalization via `pydicom` + `numpy`.
- A **PyTorch U-Net segmentation model** (`src/models/segmentation.py`) for AI-driven medical image analysis.
- A **REST API** (`src/main.py`) exposing `/analyze` and `/health` endpoints for programmatic integration.
- **Docker / docker-compose** packaging for one-command deployment on any laptop or server.

## ✨ Features

- **High Performance:** Optimized for speed and efficiency.
- **Scalable Architecture:** Designed to grow with your needs.
- **Clean Codebase:** Follows best practices and industry standards.
- **Secure by Default:** Engineered with security in mind.
- **DICOM Ingestion Pipeline:** Reads patient metadata (name, ID, modality, study description, pixel spacing) and normalizes pixel arrays to 0–255 `uint8` for downstream processing.
- **AI Segmentation Backbone:** Simplified U-Net (encoder/decoder with sigmoid output) supporting optional pretrained weight loading via `load_segmentation_model(model_path)`.
- **Production-Style API:** Async FastAPI endpoints with temporary-file cleanup and structured error handling (`HTTPException`).
- **Containerized Deployment:** Slim Python 3.11 image with system OpenGL/glib dependencies pre-installed for imaging libraries.

## 🏗️ Architecture — How It Works

```
Client (DICOM upload)
        │
        ▼
┌─────────────────────────────┐
│  FastAPI App (src/main.py)  │
│  POST /analyze  GET /health │
└─────────────┬───────────────┘
              │ saves temp_*.dcm
              ▼
┌─────────────────────────────┐
│  DICOMHandler               │
│  (src/imaging/handler.py)   │
│  • read_metadata()          │
│  • get_pixel_data()         │
│  • pixels_to_image()        │
└─────────────┬───────────────┘
              │ normalized pixel array
              ▼
┌─────────────────────────────┐
│  UNet Segmentation Model    │
│  (src/models/segmentation)  │
│  encoder → decoder → sigmoid│
└─────────────┬───────────────┘
              ▼
     JSON response: metadata + analysis
```

**Request flow (`POST /analyze`):**
1. The uploaded `.dcm` file is written to a temporary path (`temp_<filename>`).
2. `DICOMHandler.read_metadata()` extracts patient/study metadata via `pydicom`.
3. `DICOMHandler.get_pixel_data()` extracts the pixel array, clips negatives, and normalizes to 0–255.
4. (Extension point) Preprocessing + U-Net inference would run here; the current build returns a mock analysis payload.
5. The temp file is always removed in a `finally` block.

**Repository layout:**
```
├── src/
│   ├── main.py                  # FastAPI app: /analyze, /health
│   ├── imaging/handler.py       # DICOM parsing & pixel normalization
│   └── models/segmentation.py   # UNet model + loader
├── main.py                      # Standalone demo app (/predict mock)
├── Dockerfile                   # python:3.11-slim + uvicorn
├── docker-compose.yml           # single-service deployment
└── requirements.txt             # pydicom, torch, fastapi, ...
```

## 🛠️ Prerequisites

Ensure you have the following installed in your environment before proceeding:
- **Python 3.11+** (appropriate runtime for `Python`)
- Standard development tools
- **OR** Docker + Docker Compose (recommended — no local Python needed)

## 📦 Installation

Follow standard installation steps for `Python` to set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/Shivay00001/medical-imaging-dicom-viewer-ai.git
   ```
2. Navigate to the project directory:
   ```bash
   cd medical-imaging-dicom-viewer-ai
   ```
3. Install dependencies according to the standard `Python` ecosystem:
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🐳 Running with Docker (Recommended)

The repository ships with a production-ready `Dockerfile` and `docker-compose.yml`, so it runs identically on any laptop or server.

**Option A — Docker Compose (simplest):**
```bash
docker-compose up --build
```

**Option B — Plain Docker:**
```bash
docker build -t medical-imaging-ai .
docker run -p 8000:8000 -v $(pwd)/data:/app/data medical-imaging-ai
```

The API will then be available at `http://localhost:8000`. The container launches via:
```
uvicorn src.main:app --host 0.0.0.0 --port 8000
```
The `./data` directory is volume-mounted into the container for datasets/model artifacts.

## 💻 Usage

Run the project using standard execution commands for `Python`. Ensure all environment variables and configurations are set prior to execution.

**Local (without Docker):**
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Health check:**
```bash
curl http://localhost:8000/health
# → {"status": "ok"}
```

**Analyze a DICOM file:**
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@/path/to/scan.dcm"
```
Example response:
```json
{
  "status": "success",
  "metadata": {
    "patient_name": "Doe^John",
    "patient_id": "12345",
    "modality": "CT",
    "study_description": "Chest CT",
    "pixel_spacing": [0.7, 0.7]
  },
  "analysis": {"anomalies_detected": false, "message": "AI analysis completed (mock)"}
}
```

Interactive API docs are auto-generated at `http://localhost:8000/docs` (Swagger UI).

## 🔬 Workability Assessment

An honest evaluation of the current state of this repository:

**What works today:**
- ✅ The DICOM parsing layer (`DICOMHandler`) is functional and correctly normalizes pixel data.
- ✅ The FastAPI service starts, serves `/health`, and accepts DICOM uploads at `/analyze` with proper temp-file cleanup.
- ✅ Docker packaging is correct and complete — `docker-compose up` will successfully build and run the service (system deps `libgl1-mesa-glx`/`libglib2.0-0` are correctly included for imaging libs).
- ✅ The U-Net architecture is valid PyTorch and loads/evaluates correctly.

**What is NOT production-ready:**
- ⚠️ **AI inference is mocked.** The `/analyze` endpoint loads the U-Net at startup but never actually runs it — it returns a hardcoded `"mock"` analysis. Real preprocessing (resize/tensor conversion) and `model(pixels)` inference are marked as TODO.
- ⚠️ **No pretrained weights are shipped** (`.pt` files are git-ignored), and `load_segmentation_model()` is called with no path, so the model is randomly initialized — outputs would be meaningless even if wired up.
- ⚠️ **The U-Net is a toy architecture** (single down/up step, no skip connections) — not clinically meaningful as-is.
- ⚠️ **No tests exist** despite `pytest` being in requirements; there is no `tests/` directory.
- ⚠️ **No authentication, rate limiting, or PHI safeguards** — unacceptable for real patient data under HIPAA/GDPR without significant hardening.
- ⚠️ **The oversized U-Net input isn't handled** — full-resolution DICOM pixel arrays are passed with no resizing/tiling strategy.
- ⚠️ `main.py` (root) is a separate demo app with a random-number `/predict`; only `src/main.py` is served by Docker.

**Verdict:** This is a **solid architectural skeleton / prototype** — good project structure, correct containerization, and a working DICOM ingestion pipeline — but it is **not production-ready and not a functional AI viewer yet**. It requires (at minimum) wiring real inference, shipping trained weights, adding tests, and implementing security/compliance controls before any real-world or clinical use.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page. Priority areas: real inference pipeline, test coverage, and model weight management.

## 📝 License

This project is licensed under the **VisionQuantech Custom Commercial License** (see `LICENSE`):

- **Free** for personal, educational, non-earning use.
- **15–30% revenue share** required for individuals generating income from this software.
- **Business/enterprise use requires a separate commercial license** — contact **visionquantech@proton.me**.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.