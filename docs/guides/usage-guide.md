# Usage Guide

How to use Near Whisper for audio transcription.

## Starting the Application

```bash
source whisper_env/bin/activate
python whisper_gui.py
```

Open http://127.0.0.1:7860 in your browser.

## Model and Language Selection

Before transcribing, select your preferences:

### Model
Choose based on your needs:
- **Turbo**: Best for most use cases (fast + accurate)
- **Base**: Quick for short clips
- **Large**: When accuracy is critical

### Language
- Select your audio language for best results
- Use **Auto-detect** if unsure
- Supported: English, Portuguese, Spanish, French, German, Italian, Chinese, Japanese

## Transcription Methods

### Upload Audio Files
1. Click "Upload Audio Files"
2. Select one or multiple files
3. Click "Transcribe Audio"
4. Results appear in the output box

Supported formats: WAV, MP3, FLAC, OGG, M4A, and any FFmpeg-supported format.

### Record from Microphone
1. Click the microphone button to start recording
2. Speak into your microphone
3. Click stop when done
4. Click "Transcribe Audio"

## Exporting Results

### Single File
Click "Export Results" to save as a **TXT file** containing the transcription.

### Batch Upload
When transcribing multiple files, click "Export Results" to save as a **CSV file** with filename and transcription columns.

## Tips

- **Audio quality matters**: Clear recordings transcribe better
- **Language selection**: Specifying the language usually improves accuracy over auto-detect
- **Long files**: Use Turbo or Base for long recordings to save time
- **Batch processing**: Upload all files at once rather than one by one

---

[Back to Documentation](../README.md) | [Previous: Installation Guide](installation-guide.md)
