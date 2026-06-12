import os

from app.transcription import TranscriptionEngine


class TestExportTxt:
    def test_creates_file(self):
        path = TranscriptionEngine.export_txt("Hello world")
        assert path is not None
        assert os.path.exists(path)
        assert path.endswith(".txt")
        with open(path) as f:
            content = f.read()
        assert "Hello world" in content
        TranscriptionEngine.cleanup_temp(path)

    def test_empty_input_returns_none(self):
        result = TranscriptionEngine.export_txt("")
        assert result is None

    def test_none_input_returns_none(self):
        result = TranscriptionEngine.export_txt(None)
        assert result is None

    def test_unicode_content(self):
        path = TranscriptionEngine.export_txt("Olá mundo — こんにちは")
        assert path is not None
        with open(path, encoding="utf-8") as f:
            content = f.read()
        assert "Olá mundo" in content
        assert "こんにちは" in content
        TranscriptionEngine.cleanup_temp(path)


class TestExportCsv:
    def test_creates_csv(self):
        results = [
            {"filename": "a.wav", "transcription": "Hello", "language": "en", "duration": "5s"},
        ]
        path = TranscriptionEngine.export_csv(results)
        assert path is not None
        assert os.path.exists(path)
        assert path.endswith(".csv")
        TranscriptionEngine.cleanup_temp(path)

    def test_empty_input_returns_none(self):
        result = TranscriptionEngine.export_csv([])
        assert result is None

    def test_none_input_returns_none(self):
        result = TranscriptionEngine.export_csv(None)
        assert result is None

    def test_quotes_in_transcription(self):
        results = [
            {
                "filename": "a.wav",
                "transcription": 'He said "hello"',
                "language": "en",
                "duration": "3s",
            },
        ]
        path = TranscriptionEngine.export_csv(results)
        with open(path) as f:
            content = f.read()
        assert 'He said ""hello"""' in content
        TranscriptionEngine.cleanup_temp(path)

    def test_multiple_rows(self):
        results = [
            {"filename": "a.wav", "transcription": "Hello", "language": "en", "duration": "5s"},
            {"filename": "b.wav", "transcription": "World", "language": "pt", "duration": "3s"},
        ]
        path = TranscriptionEngine.export_csv(results)
        with open(path) as f:
            lines = f.readlines()
        assert len(lines) == 3
        TranscriptionEngine.cleanup_temp(path)


class TestCleanupTemp:
    def test_removes_directory(self):
        path = TranscriptionEngine.export_txt("test")
        assert os.path.exists(path)
        TranscriptionEngine.cleanup_temp(path)
        assert not os.path.exists(os.path.dirname(path))

    def test_none_input_does_not_crash(self):
        TranscriptionEngine.cleanup_temp(None)

    def test_nonexistent_path_does_not_crash(self):
        TranscriptionEngine.cleanup_temp("/tmp/nonexistent_whisper_test_12345/file.txt")


class TestTranscriptionEngineState:
    def test_initial_state(self):
        engine = TranscriptionEngine()
        assert engine.model is None
        assert engine.model_name == "base"
        assert engine.is_loaded() is False

    def test_unload_without_load(self):
        engine = TranscriptionEngine()
        success, message = engine.unload_model()
        assert success is True
        assert "No model loaded" in message
