import gradio as gr

from app.handlers import (
    clear_all,
    export_handler,
    get_model_info_html,
    get_status_html,
    load_model_handler,
    on_export_done,
    transcribe_handler,
    unload_model_handler,
)
from app.styles import CSS
from app.transcription import AVAILABLE_MODELS, LANGUAGE_OPTIONS

HEADER_HTML = """
<div class="app-header">
    <h1>Near Whisper</h1>
    <p>Free &amp; open source local audio transcription — 100% private, no internet required</p>
</div>
"""

FOOTER_HTML = """
<div class="app-footer">
    Built with <a href="https://github.com/openai/whisper" target="_blank">OpenAI Whisper</a>
    &middot;
    <a href="https://github.com/neardaniel-pls/near-whisper" target="_blank">Source on GitHub</a>
    &middot;
    MIT License
</div>
"""


def create_gui():
    with gr.Blocks(title="Near Whisper — Local Audio Transcription") as interface:
        gr.HTML(HEADER_HTML)

        with gr.Row(equal_height=True):
            # ── Sidebar ──
            with gr.Column(scale=1, min_width=280):
                gr.HTML('<div class="sidebar-section">')

                with gr.Group():
                    model_dropdown = gr.Dropdown(
                        choices=AVAILABLE_MODELS,
                        value="base",
                        label="Model",
                        info="Larger = more accurate but slower",
                    )
                    language_dropdown = gr.Dropdown(
                        choices=list(LANGUAGE_OPTIONS.keys()),
                        value="Auto-detect",
                        label="Language",
                    )

                load_btn = gr.Button("Load Model", variant="secondary", size="sm")
                eject_btn = gr.Button("Eject Model", variant="stop", size="sm")

                model_info = gr.HTML(
                    value=get_model_info_html("base"),
                    label="Model Info",
                )

                status_badge = gr.HTML(
                    value=get_status_html("Ready", "ready"),
                    label="Status",
                )

                gr.HTML("</div>")

            # ── Main Content ──
            with gr.Column(scale=3, min_width=600):
                gr.HTML('<h3 style="margin: 0 0 0.5rem; font-weight: 600;">Audio Input</h3>')

                with gr.Tabs() as tabs:
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

                gr.HTML('<hr class="section-divider">')

                transcribe_btn = gr.Button(
                    "Transcribe",
                    variant="primary",
                    size="lg",
                    elem_classes=["transcribe-btn"],
                )

                gr.HTML('<hr class="section-divider">')

                with gr.Row():
                    with gr.Column(scale=1):
                        transcription_output = gr.Textbox(
                            label="Transcription",
                            lines=16,
                            interactive=True,
                            placeholder="Transcription results will appear here...",
                            elem_classes=["output-area"],
                            buttons=["copy"],
                        )

                with gr.Row(equal_height=True):
                    export_btn = gr.Button(
                        "Export",
                        variant="secondary",
                        size="sm",
                        elem_classes=["action-btn"],
                    )
                    clear_btn = gr.Button(
                        "Clear All",
                        variant="secondary",
                        size="sm",
                        elem_classes=["action-btn"],
                    )

                download_file = gr.File(label="Download", visible=True)

        last_export_file = gr.State(value=None)

        # ── Events ──

        model_dropdown.change(
            fn=lambda m: get_model_info_html(m),
            inputs=[model_dropdown],
            outputs=[model_info],
        )

        load_btn.click(
            fn=load_model_handler,
            inputs=[model_dropdown],
            outputs=[status_badge, model_info],
        )

        eject_btn.click(
            fn=unload_model_handler,
            outputs=[status_badge],
        )

        transcribe_btn.click(
            fn=transcribe_handler,
            inputs=[audio_files, mic_input, language_dropdown, model_dropdown],
            outputs=[status_badge, transcription_output],
        )

        export_btn.click(
            fn=export_handler,
            inputs=[transcription_output],
            outputs=[download_file, status_badge],
        )

        clear_btn.click(
            fn=clear_all,
            outputs=[audio_files, mic_input, transcription_output, download_file, status_badge],
        )

        gr.HTML(FOOTER_HTML)

    return interface
