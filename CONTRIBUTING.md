# Contributing to Desktop Voice Agent

Thank you for your interest in contributing to the Desktop Voice Agent!

## Development Workflow

This project is being built incrementally through focused PRs:

1. **scaffold** - Repository structure, hotkey, tray, IPC ← Current
2. **stt** - Speech-to-text integration
3. **llm-planner** - LLM integration and planning  
4. **executor** - Task execution engine
5. **packaging** - Distribution bundles

## Getting Started

1. Fork the repository
2. Clone your fork
3. Install dependencies (see README.md)
4. Create a feature branch
5. Make your changes
6. Test your changes
7. Submit a pull request

## Code Style

### Python
- Follow PEP 8
- Use type hints where applicable
- Run `black` for formatting
- Run `flake8` for linting
- Run `mypy` for type checking

```bash
black backend/ tests/
flake8 backend/ tests/
mypy backend/
```

### Rust
- Follow standard Rust conventions
- Run `cargo fmt` before committing
- Run `cargo clippy` for linting

```bash
cargo fmt
cargo clippy
```

### TypeScript/JavaScript
- Use consistent indentation (2 spaces)
- Follow modern ES6+ conventions

## Testing

- Write tests for new features
- Ensure existing tests pass
- Run the test suite before submitting PR

```bash
# Python tests
pytest tests/ -v

# Rust tests (when available)
cargo test
```

## Commit Messages

Use clear, descriptive commit messages:

```
Add global hotkey registration for voice capture

- Implement Ctrl+Space hotkey binding
- Add notification on trigger
- Update documentation
```

## Pull Request Process

1. Update README.md with details of changes if needed
2. Update the relevant documentation
3. The PR will be reviewed and merged by maintainers

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- General questions

Thank you for contributing! 🎉
