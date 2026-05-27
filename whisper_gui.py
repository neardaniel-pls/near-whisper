#!/usr/bin/env python3
"""
Near Whisper — Local Audio Transcription
Entry point for the application.
"""

from app.gui import create_gui
from app.styles import CSS
from app.theme import create_theme


if __name__ == "__main__":
    interface = create_gui()
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        theme=create_theme(),
        css=CSS,
    )
