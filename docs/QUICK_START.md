# Quick Start Guide

Get Near Whisper running in 5 minutes.

## Prerequisites

- Fedora Linux (or any Linux with Python 3.8+)
- 4GB RAM minimum (8GB+ recommended for larger models)

## Installation

### Step 1: System Dependencies
```bash
sudo dnf install -y python3 python3-pip python3-devel ffmpeg gcc gcc-c++ make pkgconfig libsndfile-devel python3-setuptools
```

### Step 2: Virtual Environment
```bash
python3 -m venv whisper_env
source whisper_env/bin/activate
pip install --upgrade pip
```

### Step 3: Install PyTorch (CPU)
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run
```bash
python whisper_gui.py
```

Open http://127.0.0.1:7860 in your browser.

## First Transcription

1. Select **Base** model and your language (or Auto-detect)
2. Upload an audio file or use the microphone
3. Click **Transcribe Audio**
4. View the result and export if needed

## GPU Support (Optional)

For NVIDIA GPUs:
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
```

Near Whisper works perfectly on CPU — GPU is optional for faster transcription with larger models.

## Next Steps

- [Installation Guide](guides/installation-guide.md) — Detailed setup
- [Usage Guide](guides/usage-guide.md) — All features
- [FAQ](FAQ.md) — Common questions
