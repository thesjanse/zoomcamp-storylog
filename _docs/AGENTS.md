Commands

Backend, run from `backend/`:

- `uv sync` - install dependencies
- `uv run pytest` - the whole suite
- `uv run pytest tests/test_home.py` - one test file

Frontend, run from `frontend/` once it exists:

- `npm install` - install dependencies
- `npm test` - the whole Vitest suite
- `npm test -- <file>` - one test file

Rules

- Read `_docs/process.md` and your role document before starting
- Dependencies: backend dependencies go in `pyproject.toml`; frontend
  dependencies go in `package.json`. Do not add either without asking
- Do not change acceptance criteria
- Do not close issues; only the orchestrator closes an issue after QA PASS
- Do not open a PR or push unless asked

Documents

- `_docs/process.md` - how work is organized
- `_docs/tasks.md` - ordered backlog and status
- Before writing tests, read `_docs/testing-guidelines.md`
- For anything touching the UI, read `_docs/design-system.md`
