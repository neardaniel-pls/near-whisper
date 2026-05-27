import os

from app.transcription import MODEL_INFO, TranscriptionEngine


engine = TranscriptionEngine()


def get_status_html(message, state="ready"):
    color_map = {
        "ready": ("status-ready", "&#9679;"),
        "loading": ("status-loading", "&#9679;"),
        "error": ("status-error", "&#10007;"),
        "success": ("status-ready", "&#10003;"),
    }
    css_class, icon = color_map.get(state, color_map["ready"])
    return f'<div class="status-badge {css_class}"><span class="status-dot"></span> {message}</div>'


def get_model_info_html(model_name):
    info = MODEL_INFO.get(model_name)
    if not info:
        return ""

    return f"""
    <div class="model-info-card">
        <div class="info-row">
            <span class="info-label">Size</span>
            <span class="info-value">{info['size']}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Parameters</span>
            <span class="info-value">{info['params']}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Speed</span>
            <span class="info-value">{info['speed']} realtime</span>
        </div>
        <div class="info-row">
            <span class="info-label">Accuracy</span>
            <span class="info-value">{info['accuracy']}</span>
        </div>
        <div class="speed-bar">
            <div class="speed-bar-fill" style="width: {info['bar_pct']}%"></div>
        </div>
        <div class="best-for">{info['best_for']}</div>
    </div>
    """


def load_model_handler(model_name):
    info_html = get_model_info_html(model_name)
    status_html = get_status_html(f"Loading {model_name}...", "loading")
    yield status_html, info_html

    success, message = engine.load_model(model_name)

    if success:
        status_html = get_status_html(message, "success")
    else:
        status_html = get_status_html(message, "error")

    yield status_html, info_html


def unload_model_handler():
    success, message = engine.unload_model()
    state = "success" if success else "error"
    return get_status_html(message, state)


def transcribe_handler(audio_files, mic_audio, language, model_name, progress=None):
    if progress is None:
        from gradio import Progress

        progress = Progress()

    if mic_audio is not None:
        progress(0.0, desc="Starting transcription...")
        transcription, details = engine.transcribe(mic_audio, language, model_name)

        if details.get("error"):
            return get_status_html(f"Error: {details['error']}", "error"), _format_single(details)

        progress(1.0, desc="Done.")
        status = get_status_html(
            f"Done — {details['language']}, {details['duration']}", "success"
        )
        return status, _format_single(details)

    if not audio_files:
        return get_status_html("No audio provided", "error"), "Upload audio files or record audio first."

    audio_paths = [f if isinstance(f, str) else getattr(f, "name", str(f)) for f in audio_files]

    if len(audio_paths) == 1:
        progress(0.0, desc="Starting transcription...")
        transcription, details = engine.transcribe(audio_paths[0], language, model_name)

        if details.get("error"):
            return get_status_html(f"Error: {details['error']}", "error"), _format_single(details)

        progress(1.0, desc="Done.")
        status = get_status_html(
            f"Done — {details['language']}, {details['duration']}", "success"
        )
        return status, _format_single(details)

    results = []
    for i, audio_path in enumerate(progress.tqdm(audio_paths, desc="Transcribing")):
        transcription, details = engine.transcribe(audio_path, language, model_name)
        if transcription:
            results.append(
                {
                    "filename": os.path.basename(audio_path),
                    **details,
                }
            )

    if not results:
        return (
            get_status_html("No transcriptions produced", "error"),
            "No transcriptions produced. Check that the audio files are valid.",
        )

    output = f"**Processed {len(results)} file(s) successfully.**\n\n"
    for r in results:
        output += f"### {r['filename']}\n"
        output += _format_single(r)
        output += "\n---\n\n"

    status = get_status_html(f"Done — {len(results)} file(s)", "success")
    return status, output


def _format_single(details):
    if details.get("error"):
        return f"**Error:** {details['error']}\n"

    output = f"{details.get('transcription', '')}\n\n"
    output += f"| Detail | Value |\n|---|---|\n"
    output += f"| Language | {details.get('language', 'unknown')} |\n"
    output += f"| Model | {details.get('model', 'unknown')} |\n"
    output += f"| Duration | {details.get('duration', 'unknown')} |\n"
    return output


def export_handler(transcription_text):
    if not transcription_text or transcription_text.startswith("No "):
        return None, get_status_html("Nothing to export", "error")

    if "###" in transcription_text and "---" in transcription_text:
        results = _parse_batch_output(transcription_text)
        filepath = TranscriptionEngine.export_csv(results)
        if filepath:
            return filepath, get_status_html("Exported as CSV", "success")
        return None, get_status_html("Export failed", "error")

    plain_text = _strip_markdown(transcription_text)
    filepath = TranscriptionEngine.export_txt(plain_text)
    if filepath:
        return filepath, get_status_html("Exported as TXT", "success")
    return None, get_status_html("Export failed", "error")


def _parse_batch_output(text):
    results = []
    sections = text.split("---")

    for section in sections:
        lines = section.strip().split("\n")
        current = {}
        body_lines = []

        for line in lines:
            if line.startswith("### "):
                current["filename"] = line[4:].strip()
            elif "|" in line and "---" not in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) == 2:
                    key, value = parts
                    if key == "Language":
                        current["language"] = value
                    elif key == "Duration":
                        current["duration"] = value
            elif line.strip() and not line.startswith("**") and not line.startswith("Processed"):
                body_lines.append(line)

        if current and body_lines:
            current["transcription"] = "\n".join(body_lines).strip()
            results.append(current)

    return results


def _strip_markdown(text):
    lines = text.split("\n")
    clean = []
    for line in lines:
        if line.startswith("|") or line.startswith("---") or line.startswith("### "):
            continue
        clean.append(line)
    return "\n".join(clean).strip()


def clear_all():
    return (
        None,
        None,
        "",
        None,
        get_status_html("Cleared", "ready"),
    )


def on_export_done(export_path, status_html, prev_export):
    if prev_export:
        TranscriptionEngine.cleanup_temp(prev_export)
    return export_path, export_path, status_html
