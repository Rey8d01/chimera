# Repository Guidelines

This guide helps contributors work effectively on this FastAPI project.

## Project Structure & Module Organization
- `src/`: application code.
  - `src/main.py`: FastAPI app and routes.
  - `src/config.py`: settings via `pydantic-settings`.
  - `src/logger.py`: logging setup.
  - `src/database.py`: DB placeholder.
- `db/`: local SQLite data and migrations (`db/migrations/*.sql`, `db/migrate_sqlite.py`, `db/app.sqlite`).
- Tooling: `pyproject.toml`, `Makefile`, `Dockerfile`, `compose.yml`, `docker-entrypoint.sh`, `.env`.
- Docs: `README.md`. Tests live under `tests/`.

## Build, Test, and Development Commands
- Run dev server: `fastapi dev --host 0.0.0.0 --port 80 ./src/main.py` (hot reload).
- Lint: `make lint` (ruff check + autofix). Format: `make format`.
- Type check: `make type-check` (mypy, strict). All checks: `make all`.
- Clean artifacts: `make clean`.
- Docker (dev): `docker compose up --build --watch`. Docker (prod): `docker compose -f compose.yml up -d`.

## Coding Style & Naming Conventions
- Python 3.13, 4-space indent, line length 120.
- Names: `snake_case` (functions/vars), `PascalCase` (classes), `UPPER_SNAKE_CASE` (constants).
- Docstrings: PEP 257. Provide full type hints (mypy strict).
- Imports follow ruff/isort order: stdlib, third‑party, local; combine `as` imports.
- Before pushing, run `make format` and `make lint`; fix warnings.

## Testing Guidelines
- Framework: `pytest`.
- Layout: `tests/test_<module>.py`; functions start with `test_`.
- API tests: prefer `httpx.AsyncClient` with the FastAPI app.
- Run tests: `pytest -q`. Add coverage if introduced later.

## Commit & Pull Request Guidelines
- Commits: Conventional Commits (e.g., `feat(api): add health endpoint`). Keep messages clear and imperative.
- PRs: concise description, rationale, linked issues, local run steps; include example `curl` or screenshots for API changes.

## Security & Configuration Tips
- Use `.env` for local settings (e.g., `ENV`, `SQLITE_PATH`). Never commit secrets.
- Containers read env from `compose.yml` (e.g., `DB_DSN`); keep consistent with `src/config.py`.
- Before pushing: `make all` and verify the app boots locally or via `docker compose`.

