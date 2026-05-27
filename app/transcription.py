import os
import shutil
import tempfile
import threading
from datetime import datetime

import torch
import whisper


MODEL_INFO = {
    "tiny": {
        "size": "39MB",
        "params": "39M",
        "speed": "~10x",
        "accuracy": "Basic",
        "best_for": "Quick drafts",
        "bar_pct": 10,
    },
    "base": {
        "size": "74MB",
        "params": "74M",
        "speed": "~7x",
        "accuracy": "Good",
        "best_for": "Daily use",
        "bar_pct": 20,
    },
    "small": {
        "size": "244MB",
        "params": "244M",
        "speed": "~4x",
        "accuracy": "Better",
        "best_for": "Important content",
        "bar_pct": 40,
    },
    "medium": {
        "size": "769MB",
        "params": "769M",
        "speed": "~2x",
        "accuracy": "High",
        "best_for": "Professional work",
        "bar_pct": 60,
    },
    "large": {
        "size": "1550MB",
        "params": "1550M",
        "speed": "1x",
        "accuracy": "Best",
        "best_for": "Critical accuracy",
        "bar_pct": 80,
    },
    "turbo": {
        "size": "809MB",
        "params": "809M",
        "speed": "~8x",
        "accuracy": "Very Good",
        "best_for": "Fast + accurate",
        "bar_pct": 55,
    },
}

LANGUAGE_OPTIONS = {
    "Auto-detect": None,
    "English": "en",
    "Portuguese": "pt",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Chinese": "zh",
    "Japanese": "ja",
}

AVAILABLE_MODELS = list(MODEL_INFO.keys())


class TranscriptionEngine:
    def __init__(self):
        self.model = None
        self.model_name = "base"
        self._lock = threading.Lock()

    def load_model(self, model_name="base"):
        with self._lock:
            try:
                if self.model is None or self.model_name != model_name:
                    self.model_name = model_name
                    self.model = whisper.load_model(model_name)
                    return True, f"Model '{model_name}' loaded successfully."
                return True, f"Model '{model_name}' is already loaded."
            except Exception as e:
                return False, f"Error loading model: {e}"

    def unload_model(self):
        with self._lock:
            if self.model is None:
                return True, "No model loaded."
            freed_name = self.model_name
            self.model = None
            self.model_name = "base"
            return True, f"Model '{freed_name}' unloaded — memory freed."

    def is_loaded(self):
        return self.model is not None

    def transcribe(self, audio_path, language=None, model_name="base"):
        with self._lock:
            try:
                if self.model is None or self.model_name != model_name:
                    self.model_name = model_name
                    self.model = whisper.load_model(model_name)

                options = {
                    "task": "transcribe",
                    "fp16": torch.cuda.is_available(),
                }

                if language and language != "Auto-detect":
                    options["language"] = language

                result = self.model.transcribe(audio_path, **options)

                transcription = result.get("text", "")
                detected_language = result.get("language", "unknown")

                details = {
                    "transcription": transcription,
                    "language": detected_language,
                    "model": model_name,
                    "duration": (
                        f"{result['segments'][-1]['end']:.2f}s"
                        if result.get("segments")
                        else "unknown"
                    ),
                }

                return transcription, details

            except Exception as e:
                return "", {"error": str(e)}

    @staticmethod
    def export_txt(transcription, filename="transcription"):
        if not transcription:
            return None

        tmp = tempfile.mkdtemp(prefix="whisper_")
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(tmp, f"{filename}_{timestamp}.txt")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(
                    f"Transcription - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                f.write("=" * 50 + "\n\n")
                f.write(transcription)

            return filepath
        except Exception:
            shutil.rmtree(tmp, ignore_errors=True)
            return None

    @staticmethod
    def export_csv(batch_results, filename="batch_transcription"):
        if not batch_results:
            return None

        tmp = tempfile.mkdtemp(prefix="whisper_")
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(tmp, f"{filename}_{timestamp}.csv")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write("Filename,Transcription,Language,Duration\n")

                for row in batch_results:
                    text = row.get("transcription", "").replace('"', '""')
                    f.write(
                        f'"{row.get("filename", "")}","{text}",'
                        f'"{row.get("language", "")}",'
                        f'"{row.get("duration", "")}"\n'
                    )

            return filepath
        except Exception:
            shutil.rmtree(tmp, ignore_errors=True)
            return None

    @staticmethod
    def cleanup_temp(filepath):
        if filepath and os.path.exists(filepath):
            parent = os.path.dirname(filepath)
            try:
                shutil.rmtree(parent, ignore_errors=True)
            except Exception:
                pass
