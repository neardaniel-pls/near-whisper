import csv
import os

from app.handlers import (
    _format_single,
    _parse_batch_output,
    _strip_markdown,
    clear_all,
    export_handler,
    get_model_info_html,
    get_status_html,
    on_export_done,
)
from app.transcription import AVAILABLE_MODELS, LANGUAGE_OPTIONS, MODEL_INFO


class TestGetStatusHtml:
    def test_ready_state(self):
        html = get_status_html("Ready", "ready")
        assert "status-ready" in html
        assert "Ready" in html

    def test_loading_state(self):
        html = get_status_html("Loading...", "loading")
        assert "status-loading" in html
        assert "Loading..." in html

    def test_error_state(self):
        html = get_status_html("Error occurred", "error")
        assert "status-error" in html
        assert "Error occurred" in html

    def test_success_state(self):
        html = get_status_html("Done", "success")
        assert "status-success" in html
        assert "Done" in html

    def test_unknown_state_defaults_to_ready(self):
        html = get_status_html("Unknown", "nonexistent")
        assert "status-ready" in html

    def test_default_state_is_ready(self):
        html = get_status_html("Test")
        assert "status-ready" in html


class TestGetModelInfoHtml:
    def test_valid_model(self):
        html = get_model_info_html("base")
        assert "74MB" in html
        assert "74M" in html
        assert "Daily use" in html

    def test_turbo_model(self):
        html = get_model_info_html("turbo")
        assert "809MB" in html
        assert "Fast + accurate" in html

    def test_invalid_model_returns_empty(self):
        html = get_model_info_html("nonexistent")
        assert html == ""

    def test_all_models_have_info(self):
        for model in AVAILABLE_MODELS:
            html = get_model_info_html(model)
            assert html != "", f"Missing info for model '{model}'"


class TestFormatSingle:
    def test_with_error(self):
        result = _format_single({"error": "Something went wrong"})
        assert "**Error:**" in result
        assert "Something went wrong" in result

    def test_with_transcription(self):
        details = {
            "transcription": "Hello world",
            "language": "en",
            "model": "base",
            "duration": "5.23s",
        }
        result = _format_single(details)
        assert "Hello world" in result
        assert "| Language | en |" in result
        assert "| Model | base |" in result
        assert "| Duration | 5.23s |" in result

    def test_missing_fields_show_unknown(self):
        result = _format_single({"transcription": "text"})
        assert "unknown" in result


class TestParseBatchOutput:
    def test_single_section(self):
        text = "### file1.wav\nTranscribed text here.\n| Language | en |\n| Duration | 5s |\n---\n"
        results = _parse_batch_output(text)
        assert len(results) == 1
        assert results[0]["filename"] == "file1.wav"
        assert results[0]["language"] == "en"
        assert results[0]["duration"] == "5s"
        assert "Transcribed text here." in results[0]["transcription"]

    def test_multiple_sections(self):
        text = (
            "### a.wav\nText A\n| Language | en |\n---\n\n"
            "### b.wav\nText B\n| Language | pt |\n---\n"
        )
        results = _parse_batch_output(text)
        assert len(results) == 2
        assert results[0]["filename"] == "a.wav"
        assert results[1]["filename"] == "b.wav"

    def test_empty_input(self):
        results = _parse_batch_output("")
        assert results == []


class TestStripMarkdown:
    def test_removes_tables(self):
        text = "Hello\n| h1 | h2 |\n|---|---|\n| a | b |\nWorld"
        result = _strip_markdown(text)
        assert "|" not in result
        assert "Hello" in result
        assert "World" in result

    def test_removes_headings(self):
        text = "### Title\nContent here"
        result = _strip_markdown(text)
        assert "###" not in result
        assert "Content here" in result

    def test_removes_hr(self):
        text = "Above\n---\nBelow"
        result = _strip_markdown(text)
        assert "---" not in result


class TestExportHandler:
    def test_empty_text(self):
        result, status = export_handler("")
        assert result is None
        assert "Nothing to export" in status

    def test_no_audio_text(self):
        result, status = export_handler("No audio provided. Upload files first.")
        assert result is None

    def test_single_transcription_exports_txt(self):
        text = "Hello world\n\n| Language | en |\n| Model | base |\n| Duration | 5s |\n"
        result, status = export_handler(text)
        assert result is not None
        assert result.endswith(".txt")
        assert os.path.exists(result)
        assert "Exported as TXT" in status
        with open(result) as f:
            content = f.read()
        assert "Hello world" in content

    def test_batch_transcription_exports_csv(self):
        text = (
            "**Processed 2 file(s) successfully.**\n\n"
            "### a.wav\nTranscript A\n| Language | en |\n| Duration | 3s |\n---\n\n"
            "### b.wav\nTranscript B\n| Language | pt |\n| Duration | 4s |\n---\n"
        )
        result, status = export_handler(text)
        assert result is not None
        assert result.endswith(".csv")
        assert os.path.exists(result)
        assert "Exported as CSV" in status
        with open(result) as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert rows[0][0] == "Filename"
        assert len(rows) == 3


class TestClearAll:
    def test_returns_expected_tuple(self):
        result = clear_all()
        assert len(result) == 6
        assert result[0] is None
        assert result[1] is None
        assert result[2] == ""
        assert result[3] is None
        assert "Cleared" in result[4]
        assert result[5] is None


class TestOnExportDone:
    def test_cleans_up_previous_export(self, tmp_path):
        old_dir = tmp_path / "old_export"
        old_dir.mkdir()
        old_file = old_dir / "old.txt"
        old_file.write_text("old")

        new_path = "/some/new/path.txt"
        status = get_status_html("Done", "success")
        old_path = str(old_file)

        result_path, result_state, result_status = on_export_done(
            new_path, status, old_path
        )
        assert result_path == new_path
        assert result_state == new_path
        assert not old_dir.exists()


class TestModelInfo:
    def test_all_models_have_required_keys(self):
        required = {"size", "params", "speed", "accuracy", "best_for", "bar_pct"}
        for model, info in MODEL_INFO.items():
            assert required.issubset(info.keys()), f"Missing keys in '{model}'"

    def test_available_models_matches_info(self):
        assert AVAILABLE_MODELS == list(MODEL_INFO.keys())


class TestLanguageOptions:
    def test_auto_detect_is_none(self):
        assert LANGUAGE_OPTIONS["Auto-detect"] is None

    def test_has_expected_languages(self):
        expected = {
            "English", "Portuguese", "Spanish", "French",
            "German", "Italian", "Chinese", "Japanese",
        }
        assert expected.issubset(set(LANGUAGE_OPTIONS.keys()))
