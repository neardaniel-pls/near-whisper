# Installation Guide

Detailed installation instructions for Near Whisper.

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.8+ | 3.11+ |
| RAM | 4GB | 8GB+ |
| Storage | 2GB | 5GB+ (for models) |
| GPU | Not required | NVIDIA with CUDA (optional) |

## Step-by-Step Installation

### 1. Install System Dependencies

**Fedora:**
```bash
sudo dnf install -y python3 python3-pip python3-devel ffmpeg gcc gcc-c++ make pkgconfig libsndfile-devel python3-setuptools
```

**Ubuntu/Debian:**
```bash
sudo apt install -y python3 python3-pip python3-dev ffmpeg gcc g++ make pkg-config libsndfile1-dev python3-setuptools
```

### 2. Create Virtual Environment

```bash
python3 -m venv whisper_env
source whisper_env/bin/activate
pip install --upgrade pip
```

### 3. Install PyTorch

**CPU only (recommended for most users):**
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**NVIDIA GPU with CUDA 12.4:**
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python whisper_gui.py
```

Open http://127.0.0.1:7860 in your browser.

## Model Selection

Models are downloaded automatically on first use:

| Model | Size | RAM Needed | Best For |
|-------|------|------------|----------|
| Tiny | 39MB | 1GB | Quick drafts |
| Base | 74MB | 1GB | Daily use |
| Small | 244MB | 2GB | Important content |
| Medium | 769MB | 5GB | Professional work |
| Large | 1550MB | 8GB+ | Maximum accuracy |
| Turbo | 809MB | 4GB | Fast + accurate |

**Recommendation**: Start with **Turbo** for the best balance of speed and accuracy on CPU.

## Troubleshooting Installation

### FFmpeg build issues
Ensure `ffmpeg` is installed: `sudo dnf install ffmpeg`.

### Torch installation fails
Try installing CPU-only version first. If you need GPU support, ensure you have the correct CUDA toolkit version.

### Permission denied on venv
Don't use `sudo` with pip inside the virtual environment. Activate the venv first.

---

[Back to Documentation](../README.md) | [Next: Usage Guide](usage-guide.md)
