#!/usr/bin/env python3
"""
Local Whisper GUI - FOSS Audio Transcription Tool
A free and open source GUI for local Whisper transcription on Fedora
Supports single/batch file upload, microphone recording, and multiple languages
"""

import os
import shutil
import tempfile
import threading
from datetime import datetime
from pathlib import Path

import gradio as gr
import whisper
import torch


class LocalWhisperGUI:
    """Main application class for Local Whisper GUI"""

    def __init__(self):
        """Initialize the GUI application"""
        self.model = None
        self.model_name = "base"
        self.sample_rate = 16000
        self._lock = threading.Lock()

        self.available_models = ["tiny", "base", "small", "medium", "large", "turbo"]

        self.language_options = {
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

    def load_model(self, model_name="base"):
        """Load Whisper model

        Args:
            model_name (str): Name of the model to load

        Returns:
            str: Status message
        """
        with self._lock:
            try:
                if self.model is None or self.model_name != model_name:
                    self.model_name = model_name
                    self.model = whisper.load_model(model_name)
                    return f"Model '{model_name}' loaded successfully."
                return f"Model '{model_name}' is already loaded."
            except Exception as e:
                return f"Error loading model: {e}"

    def transcribe_audio(self, audio_path, language=None, model_name="base"):
        """Transcribe audio file using local Whisper

        Args:
            audio_path (str): Path to the audio file
            language (str): Language code or None for auto-detection
            model_name (str): Model name to use for transcription

        Returns:
            tuple: (transcription_text, details_text)
        """
        with self._lock:
            try:
                if self.model is None or self.model_name != model_name:
                    self.load_model(model_name)

                options = {
                    "task": "transcribe",
                    "fp16": torch.cuda.is_available(),
                }

                if language and language != "Auto-detect":
                    options["language"] = language

                result = self.model.transcribe(audio_path, **options)

                transcription = result.get("text", "")
                detected_language = result.get("language", "unknown")

                output = f"**Transcription:**\n{transcription}\n\n"
                output += f"**Detected Language:** {detected_language}\n"
                output += f"**Model Used:** {model_name}\n"

                if result.get("segments"):
                    output += f"**Duration:** {result['segments'][-1]['end']:.2f} seconds\n"

                return transcription, output

            except Exception as e:
                error_msg = f"Transcription error: {e}"
                return "", error_msg

    def export_transcription(self, transcription, filename="transcription"):
        """Export transcription to text file

        Args:
            transcription (str): Transcription text to export
            filename (str): Base filename for the export

        Returns:
            str: Path to exported file or None
        """
        if not transcription:
            return None

        tmp = tempfile.mkdtemp(prefix="whisper_")
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(tmp, f"{filename}_{timestamp}.txt")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Transcription - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                f.write(transcription)

            return filepath
        except Exception:
            shutil.rmtree(tmp, ignore_errors=True)
            return None

    def export_batch_results(self, batch_results, filename="batch_transcription"):
        """Export batch transcription results to CSV file

        Args:
            batch_results (list): List of result rows [filename, transcription, language, duration]
            filename (str): Base filename for the export

        Returns:
            str: Path to exported file or None
        """
        if not batch_results:
            return None

        tmp = tempfile.mkdtemp(prefix="whisper_")
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(tmp, f"{filename}_{timestamp}.csv")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write("Filename,Transcription,Language,Duration\n")

                for row in batch_results:
                    text = row[1].replace('"', '""') if len(row) > 1 else ""
                    f.write(
                        f'"{row[0]}","{text}",'
                        f'"{row[2] if len(row) > 2 else ""}",'
                        f'"{row[3] if len(row) > 3 else ""}"\n'
                    )

            return filepath
        except Exception:
            shutil.rmtree(tmp, ignore_errors=True)
            return None

    def cleanup_temp(self, filepath):
        """Clean up temporary directory created for an export file

        Args:
            filepath (str): Path to the exported file whose parent dir should be removed
        """
        if filepath and os.path.exists(filepath):
            parent = os.path.dirname(filepath)
            try:
                shutil.rmtree(parent, ignore_errors=True)
            except Exception:
                pass


def create_gui():
    """Create and configure the Gradio interface

    Returns:
        gr.Blocks: Configured Gradio interface
    """
    app = LocalWhisperGUI()

    with gr.Blocks(title="Local Whisper GUI") as interface:
        gr.Markdown("# Local Whisper GUI")
        gr.Markdown("Free and open source audio transcription using local Whisper models.")

        with gr.Row():
            with gr.Column(scale=1):
                model_dropdown = gr.Dropdown(
                    choices=app.available_models,
                    value="base",
                    label="Model Size",
                    info="Larger = more accurate but slower. Turbo is fast and accurate.",
                )
                language_dropdown = gr.Dropdown(
                    choices=list(app.language_options.keys()),
                    value="Auto-detect",
                    label="Language",
                )
                load_btn = gr.Button("Load Model", variant="secondary")

            with gr.Column(scale=1):
                model_status = gr.Textbox(
                    label="Status", value="Ready — select a model and upload or record audio.", interactive=False
                )

        gr.Markdown("### Audio Input")

        with gr.Tabs():
            with gr.Tab("Upload Files"):
                audio_files = gr.File(
                    label="Select audio files",
                    file_count="multiple",
                    file_types=["audio"],
                    type="filepath",
                )

            with gr.Tab("Microphone"):
                mic_input = gr.Audio(
                    label="Record audio",
                    sources=["microphone"],
                    type="filepath",
                )

        transcribe_btn = gr.Button("Transcribe", variant="primary", size="lg")

        with gr.Row():
            with gr.Column():
                transcription_output = gr.Textbox(
                    label="Results",
                    lines=15,
                    interactive=True,
                    placeholder="Transcription results will appear here...",
                )

                with gr.Row():
                    export_btn = gr.Button("Export")
                    clear_btn = gr.Button("Clear All")

        last_export_file = gr.State(value=None)

        def load_model_handler(model_name):
            """Handle model loading button click"""
            return app.load_model(model_name)

        def transcribe_handler(audio_files, mic_audio, language, model_name, progress=gr.Progress()):
            """Handle transcription for both file upload and microphone input

            Args:
                audio_files: List of uploaded files or None
                mic_audio: Microphone audio path or None
                language: Selected language
                model_name: Selected model
                progress: Gradio progress tracker

            Returns:
                str: Formatted transcription results
            """
            if mic_audio is not None:
                progress(0.0, desc="Starting transcription...")
                transcription, details = app.transcribe_audio(mic_audio, language, model_name)
                progress(1.0, desc="Done.")
                return details

            if not audio_files:
                return "Please upload audio files or record audio first."

            audio_paths = [f if isinstance(f, str) else getattr(f, "name", str(f)) for f in audio_files]

            if len(audio_paths) == 1:
                progress(0.0, desc="Starting transcription...")
                transcription, details = app.transcribe_audio(audio_paths[0], language, model_name)
                progress(1.0, desc="Done.")
                return details

            results = []
            for i, audio_path in enumerate(progress.tqdm(audio_paths, desc="Transcribing")):
                transcription, details = app.transcribe_audio(audio_path, language, model_name)
                if transcription:
                    results.append(
                        {
                            "filename": os.path.basename(audio_path),
                            "transcription": transcription,
                            "details": details,
                        }
                    )

            if not results:
                return "No transcriptions produced. Check that the audio files are valid."

            output_text = f"Processed {len(results)} file(s) successfully.\n\n"
            for r in results:
                output_text += f"FILE: {r['filename']}\n{r['details']}\n\n{'─' * 50}\n\n"
            return output_text

        def export_handler(transcription_text):
            """Export transcription results to file

            Automatically detects single file vs batch result
            and exports as TXT or CSV accordingly.

            Args:
                transcription_text (str): Formatted transcription text

            Returns:
                tuple: (file_path_or_None, status_message)
            """
            if not transcription_text or transcription_text.startswith("Please") or transcription_text.startswith("No "):
                return None, ""

            if "FILE:" in transcription_text and "─" * 20 in transcription_text:
                lines = transcription_text.split("\n")
                results = []
                current = {}

                for line in lines:
                    if line.startswith("FILE:"):
                        if current:
                            results.append(current)
                        current = {"filename": line[5:].strip()}
                    elif line.startswith("**Detected Language:"):
                        current["language"] = line.split(":", 1)[1].strip()
                    elif line.startswith("**Duration:"):
                        current["duration"] = line.split(":", 1)[1].strip()
                    elif line.startswith("─"):
                        if current:
                            results.append(current)
                            current = {}
                    elif current and not line.startswith("**") and line.strip() and not line.startswith("Processed"):
                        current["transcription"] = current.get("transcription", "") + line + "\n"

                if current:
                    results.append(current)

                df_data = [
                    [
                        r.get("filename", ""),
                        r.get("transcription", "").strip(),
                        r.get("language", ""),
                        r.get("duration", ""),
                    ]
                    for r in results
                ]
                return app.export_batch_results(df_data), "Batch results exported as CSV."
            else:
                return app.export_transcription(transcription_text), "Transcription exported as TXT."

        def clear_all():
            """Clear all inputs, outputs, and export file"""
            return None, None, "", None, "Cleared."

        def on_export_done(export_path, status_msg, prev_export):
            """Clean up previous temp export and store new one"""
            if prev_export:
                app.cleanup_temp(prev_export)
            return export_path, export_path, status_msg

        load_btn.click(load_model_handler, inputs=[model_dropdown], outputs=[model_status])

        transcribe_btn.click(
            transcribe_handler,
            inputs=[audio_files, mic_input, language_dropdown, model_dropdown],
            outputs=[transcription_output],
        )

        export_result = export_btn.click(
            export_handler,
            inputs=[transcription_output],
            outputs=[gr.File(label="Download"), model_status],
        )

        clear_btn.click(
            clear_all,
            outputs=[audio_files, mic_input, transcription_output, gr.File(label="Download"), model_status],
        )

    return interface


if __name__ == "__main__":
    interface = create_gui()
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        theme=gr.themes.Soft(),
    )
