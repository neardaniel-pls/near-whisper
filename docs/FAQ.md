# Frequently Asked Questions

## General

### Does it work without internet?
Yes, after initial setup. Model downloads happen once. After that, all processing is local.

### Is my audio data private?
Yes. All processing happens on your machine. No audio is sent to any server.

### Does it work on non-Fedora systems?
Yes, it should work on any Linux system with Python 3.8+. macOS and Windows may also work but are untested.

## Models

### Which model should I use?
- **Tiny/Base**: Fast, good for quick drafts
- **Turbo**: Best balance of speed and accuracy (recommended for CPU)
- **Large**: Best accuracy but slow on CPU

### Where are models stored?
PyTorch Whisper models are cached in `~/.cache/whisper/`.

### Can I use a GPU?
Yes, if you have an NVIDIA GPU with CUDA. Install PyTorch with CUDA support instead of the CPU version. See [Installation Guide](guides/installation-guide.md).

## Audio

### What formats are supported?
Any format supported by FFmpeg: WAV, MP3, FLAC, OGG, M4A, etc.

### How long can recordings be?
Limited only by your RAM. For very long files, the Large model may require 8GB+ RAM.

### Can I transcribe multiple files at once?
Yes. Use the "Upload Audio Files" tab to select multiple files. Results are shown for each file, and you can export all as CSV.

## Troubleshooting

### PortAudio error
```bash
sudo dnf install portaudio-devel
```

### FFmpeg not found
```bash
sudo dnf install ffmpeg
```

### Out of memory with Large model
Try a smaller model (Turbo or Medium). The Large model requires significant RAM.

### Model download fails
Check your internet connection. Models are downloaded from Hugging Face on first use.

---

**Last Updated**: 2026-05-25
