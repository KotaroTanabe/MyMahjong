# Agent Instructions

- Always write tests covering your changes whenever practical.
- Document the current implementation status in `README.md`.
  Include which packages and features exist and which remain unimplemented.
  Use markdown checklists (`- [x]`/`- [ ]`). This is not required for bugfixes.
- Before opening a PR, install dependencies and run the same checks as CI:
  1. `uv pip install -e ./core -e ./cli -e ./web`
  2. `uv pip install flake8 mypy pytest build`
  3. `python -m build core`
  4. `python -m build cli`
  5. `flake8`
  6. `mypy core web cli`
  7. `pytest -q`
  8. `npm ci` in `web_gui`
  9. `npx vitest run` in `web_gui`
