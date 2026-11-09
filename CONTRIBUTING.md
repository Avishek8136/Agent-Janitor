# Contributing to Agent Janitor

Thank you for your interest in improving `agent-janitor`! We welcome contributions to help keep codebases clean and distraction-free for AI coding agents.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/agent-janitor.git
   cd agent-janitor
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install in editable mode with development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## Running Tests

Run the test suite using Python's built-in `unittest`:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Running the Distraction Audit on Itself
Ensure no dead-end traps or distraction hazards exist in this repository:
```bash
agent-janitor audit .
agent-janitor check .
```

## Code Style & Guidelines

- **Zero Unprompted Side-Quests:** Follow the strict scope guidelines outlined in `rules/agent-focus.md`.
- **Typing:** Provide explicit type annotations on public functions and dataclasses.
- **Cross-Platform Compatibility:** Ensure path handling uses `pathlib.Path` and handles Windows/POSIX paths cleanly.
- **No External Dependencies for Core Runtime:** Keep the scanner, classifier, cleaner, and stdio MCP server free of heavy dependencies so it can run instantly anywhere.

## Submitting Pull Requests

1. Fork the repo and create a new feature branch (`git checkout -b feat/my-improvement`).
2. Add unit tests for your changes in `tests/`.
3. Verify all tests pass and `git diff` is clean.
4. Commit your changes using Conventional Commits (`feat: ...`, `fix: ...`, `docs: ...`).
5. Open a Pull Request describing the motivation and impact of the change.
