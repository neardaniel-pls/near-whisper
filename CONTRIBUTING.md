# Contributing

1. Fork the repo at https://github.com/neardaniel-pls/near-whisper
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Push and open a pull request

## Code Style

- Follow PEP 8
- Use type hints for function signatures
- Keep GUI code in `app/` directory
- Entry point is `whisper_gui.py`
- Test with at least one model (tiny or base) before submitting

## Testing

- Run the application: `python whisper_gui.py`
- Test with microphone recording and file upload
- Test batch upload with multiple files
- Verify export (TXT and CSV)

## Commit Messages

Use conventional commits: `feat`, `fix`, `docs`, `refactor`, `chore`
