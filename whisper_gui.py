#!/usr/bin/env python3
"""
Local Whisper GUI - FOSS Audio Transcription Tool
A free and open source GUI for local Whisper transcription on Fedora
Supports single/batch file upload, microphone recording, and multiple languages
"""

import os
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path

import gradio as gr
import whisper
import torch
import numpy as np
from scipy.io import wavfile
import librosa
from tqdm import tqdm

class LocalWhisperGUI:
    """Main application class for Local Whisper GUI"""
    
    def __init__(self):
        """Initialize the GUI application"""
        self.model = None
        self.model_name = "base"
        self.sample_rate = 16000  # Whisper's preferred sample rate
        
        # Available models (including newer ones)
        self.available_models = ["tiny", "base", "small", "medium", "large", "turbo"]
        
        # Language options
        self.language_options = {
            "Auto-detect": None,
            "English": "en",
            "Portuguese": "pt",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Italian": "it",
            "Chinese": "zh",
            "Japanese": "ja"
        }
        
        # Load model on startup
        self.load_model()
    
    def load_model(self, model_name="base"):
        """Load Whisper model
        
        Args:
            model_name (str): Name of the model to load
            
        Returns:
            str: Status message
        """
        try:
            if self.model is None or self.model_name != model_name:
                self.model_name = model_name
                self.model = whisper.load_model(model_name)
                return f"✅ Model '{model_name}' loaded successfully!"
            return f"✅ Model '{model_name}' already loaded"
        except Exception as e:
            return f"❌ Error loading model: {str(e)}"
    
    def transcribe_audio(self, audio_path, language=None, model_name="base"):
        """Transcribe audio file using local Whisper
        
        Args:
            audio_path (str): Path to the audio file
            language (str): Language code or None for auto-detection
            model_name (str): Model name to use for transcription
            
        Returns:
            tuple: (transcription_text, details_text)
        """
        try:
            # Load model if needed
            if self.model is None or self.model_name != model_name:
                self.load_model(model_name)
            
            # Prepare options
            options = {
                "task": "transcribe",
                "fp16": torch.cuda.is_available(),  # Use FP16 if GPU available
            }
            
            # Add language if specified
            if language and language != "Auto-detect":
                options["language"] = language
            
            # Transcribe
            result = self.model.transcribe(audio_path, **options)
            
            # Format result
            transcription = result.get("text", "")
            detected_language = result.get("language", "unknown")
            
            # Create detailed output
            output = f"**Transcription:**\n{transcription}\n\n"
            output += f"**Detected Language:** {detected_language}\n"
            output += f"**Model Used:** {model_name}\n"
            
            if result.get("segments"):
                output += f"**Duration:** {result['segments'][-1]['end']:.2f} seconds\n"
            
            return transcription, output
            
        except Exception as e:
            error_msg = f"❌ Transcription error: {str(e)}"
            return "", error_msg
    
    def transcribe_multiple_files(self, audio_files, language=None, model_name="base"):
        """Transcribe multiple audio files
        
        Args:
            audio_files (list): List of audio file paths
            language (str): Language code or None for auto-detection
            model_name (str): Model name to use for transcription
            
        Returns:
            list: List of transcription results
        """
        results = []
        
        for i, audio_path in enumerate(audio_files):
            transcription, details = self.transcribe_audio(audio_path, language, model_name)
            if transcription:
                results.append({
                    "filename": os.path.basename(audio_path),
                    "transcription": transcription,
                    "details": details
                })
        
        return results
    
    def process_gradio_audio(self, audio_file):
        """Process audio from Gradio's audio component"""
        if audio_file is None:
            return "", "❌ No audio provided"
        
        return self.transcribe_audio(audio_file, None, self.model_name)
    
    def export_transcription(self, transcription, filename="transcription"):
        """Export transcription to text file"""
        if not transcription:
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_with_timestamp = f"{filename}_{timestamp}.txt"
            
            temp_dir = tempfile.mkdtemp()
            filepath = os.path.join(temp_dir, filename_with_timestamp)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Transcription - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                f.write(transcription)
            
            return filepath
            
        except Exception as e:
            print(f"Export error: {e}")
            return None
    
    def export_batch_results(self, batch_results, filename="batch_transcription"):
        """Export batch transcription results to CSV file"""
        if batch_results is None or (hasattr(batch_results, 'empty') and batch_results.empty):
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_with_timestamp = f"{filename}_{timestamp}.csv"
            
            temp_dir = tempfile.mkdtemp()
            filepath = os.path.join(temp_dir, filename_with_timestamp)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                # Write CSV header
                f.write("Filename,Transcription,Language,Duration\n")
                
                # Write data rows
                for row in batch_results:
                    # Escape commas and quotes in transcription
                    transcription = row[1].replace('"', '""') if len(row) > 1 else ""
                    f.write(f'"{row[0]}","{transcription}","{row[2] if len(row) > 2 else ""}","{row[3] if len(row) > 3 else ""}"\n')
            
            return filepath
            
        except Exception as e:
            print(f"Batch export error: {e}")
            return None

def create_gui():
    """Create and configure the Gradio interface
    
    Returns:
        gr.Blocks: Configured Gradio interface
    """
    app = LocalWhisperGUI()
    
    with gr.Blocks(title="Local Whisper GUI", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🎤 Local Whisper GUI")
        gr.Markdown("Free and open source audio transcription using local Whisper models")
        
        with gr.Row():
            with gr.Column(scale=2):
                # Model selection
                model_dropdown = gr.Dropdown(
                    choices=app.available_models,
                    value="base",
                    label="Model Size",
                    info="Larger models are more accurate but slower. turbo & large-v3 are newer, faster models"
                )
                
                # Language selection
                language_dropdown = gr.Dropdown(
                    choices=list(app.language_options.keys()),
                    value="Auto-detect",
                    label="Language"
                )
                
                # Model status
                model_status = gr.Textbox(
                    label="Model Status",
                    value="Loading model...",
                    interactive=False
                )
            
            with gr.Column(scale=1):
                # Load model button
                load_btn = gr.Button("Load Model", variant="primary")
        
        # Audio input section
        with gr.Row():
            with gr.Column(scale=2):
                # Audio file input (supports both single and multiple files)
                audio_files = gr.File(
                    label="Upload Audio Files (single or multiple)",
                    file_count="multiple",
                    file_types=["audio"],
                    type="filepath"
                )
                
                # Microphone input
                mic_input = gr.Audio(
                    label="Or Record Audio",
                    sources=["microphone"],
                    type="filepath"
                )
            
            with gr.Column(scale=1):
                # Transcription buttons
                transcribe_btn = gr.Button("Transcribe Audio", variant="primary")
                clear_btn = gr.Button("Clear All")
        
        # Output section
        with gr.Row():
            with gr.Column():
                # Unified transcription output (can show single or multiple results)
                transcription_output = gr.Textbox(
                    label="Transcription Results",
                    lines=15,
                    interactive=True
                )
                
                # Export button
                with gr.Row():
                    export_btn = gr.Button("Export Results")
                    clear_output_btn = gr.Button("Clear Output")
        
        # Event handlers
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
            # Handle microphone input first
            if mic_audio is not None:
                print("Transcribing microphone recording...")
                progress(0.0, desc="Starting transcription")
                transcription, details = app.transcribe_audio(mic_audio, language, model_name)
                progress(1.0, desc="Transcription complete")
                return f"{details}"
            
            # Handle file input
            if not audio_files:
                return "❌ Please upload audio files or record audio"
            
            # Extract file paths from gradio File objects
            audio_paths = [f.name for f in audio_files]
            
            # Check if it's a single file or multiple files
            if len(audio_paths) == 1:
                print(f"Transcribing file: {os.path.basename(audio_paths[0])}")
                progress(0.0, desc="Starting transcription")
                transcription, details = app.transcribe_audio(audio_paths[0], language, model_name)
                progress(1.0, desc="Transcription complete")
                return f"{details}"
            else:
                # Process multiple files with progress
                results = []
                for i, audio_path in enumerate(progress.tqdm(audio_paths, desc="Transcribing files")):
                    print(f"Processing file {i+1}/{len(audio_paths)}: {os.path.basename(audio_path)}")
                    transcription, details = app.transcribe_audio(audio_path, language, model_name)
                    if transcription:
                        results.append({
                            "filename": os.path.basename(audio_path),
                            "transcription": transcription,
                            "details": details
                        })
                
                # Format results for display
                output_text = f"✅ Processed {len(results)} files successfully\n\n"
                
                for result in results:
                    output_text += f"FILE: {result.get('filename', '')}\n"
                    output_text += f"{result.get('details', '')}\n\n"
                    output_text += "-" * 50 + "\n\n"
                
                return output_text
        
        def export_handler(transcription_text):
            """Export transcription results to file
            
            Automatically detects if it's a single file or batch result
            and exports as TXT or CSV accordingly.
            
            Args:
                transcription_text (str): Formatted transcription text
                
            Returns:
                str: Path to exported file or None
            """
            if not transcription_text:
                return None
            
            # Check if this is a batch result (contains multiple files)
            if "FILE:" in transcription_text and "-" * 50 in transcription_text:
                # Extract batch results and export as CSV
                lines = transcription_text.split('\n')
                results = []
                current_file = {}
                
                for line in lines:
                    if line.startswith("FILE:"):
                        if current_file:  # Save previous file if exists
                            results.append(current_file)
                        current_file = {"filename": line[5:].strip()}
                    elif line.startswith("**Detected Language:"):
                        current_file["language"] = line.split(":", 1)[1].strip()
                    elif line.startswith("**Duration:"):
                        current_file["duration"] = line.split(":", 1)[1].strip()
                    elif line.startswith("✅ Processed"):
                        # Summary line, skip
                        continue
                    elif line.startswith("-" * 50):
                        # End of file section
                        if current_file:
                            # Collect all transcription text
                            if "transcription" not in current_file:
                                current_file["transcription"] = ""
                            results.append(current_file)
                            current_file = {}
                    elif current_file and not line.startswith("**") and line.strip():
                        # Transcription text
                        if "transcription" in current_file:
                            current_file["transcription"] += line + "\n"
                        else:
                            current_file["transcription"] = line + "\n"
                
                # Convert to CSV format
                df_data = []
                for result in results:
                    df_data.append([
                        result.get("filename", ""),
                        result.get("transcription", "").strip(),
                        result.get("language", ""),
                        result.get("duration", "")
                    ])
                
                return app.export_batch_results(df_data)
            else:
                # Single file transcription, export as text
                return app.export_transcription(transcription_text)
        
        # Connect events
        load_btn.click(
            load_model_handler,
            inputs=[model_dropdown],
            outputs=[model_status]
        )
        
        # Unified transcribe button
        transcribe_btn.click(
            transcribe_handler,
            inputs=[audio_files, mic_input, language_dropdown, model_dropdown],
            outputs=[transcription_output]
        )
        
        # Clear button
        clear_btn.click(
            lambda: (None, None, ""),
            outputs=[audio_files, mic_input, transcription_output]
        )
        
        # Export button
        export_btn.click(
            export_handler,
            inputs=[transcription_output],
            outputs=[gr.File()]
        )
        
        clear_output_btn.click(
            lambda: "",
            outputs=[transcription_output]
        )
        
        # Load initial model
        interface.load(
            load_model_handler,
            inputs=[gr.Textbox(value="base", visible=False)],
            outputs=[model_status]
        )
    
    return interface

if __name__ == "__main__":
    # Create and launch the GUI
    interface = create_gui()
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )