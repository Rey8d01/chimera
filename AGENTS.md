# Repository Guidelines

This guide keeps contributions aligned with the FastAPI codebase and tooling.

## Project Structure & Module Organization
- `src/` holds production code; key modules are `src/main.py` (app bootstrap), `src/auth/*` (auth flows), `src/config.py` (settings), and `src/database.py` (SQLite connection management).
- `tests/` mirrors feature areas using async HTTP clients; fixtures live in `tests/conftest.py`.
- `db/` stores migrations and local data (`db/migrations/*.sql`, `db/migrate_sqlite.py`, `db/data/app.sqlite`).
- Tooling and container assets: `pyproject.toml`, `Makefile`, `Dockerfile`, `compose.yml`, `docker-entrypoint.sh`, `.env`.

## Build, Test, and Development Commands
- Dev server with hot reload: `fastapi dev --host 0.0.0.0 --port 80 ./src/main.py`.
- Quality gates: `make lint` (Ruff auto-fix), `make format` (Ruff formatter), `make type-check` (mypy + ty), `make all` (runs the trio).
- Execute tests: `make test` or `pytest -q`. Target suites with `make test TESTS=tests/auth/test_router.py` or add filters via `make test PYTEST_ARGS="-k login"`.
- Containers: iterative development `docker compose up --build --watch`; production-like `docker compose -f compose.yml up -d`.

## Coding Style & Naming Conventions
- Python 3.13, four-space indentation, max line length 120.
- Naming defaults: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
- Require PEP 257 docstrings where context is non-trivial and provide complete type hints (strict mypy).
- Respect import order (stdlib, third-party, local) and run `make format && make lint` before pushing.

## Testing Guidelines
- Primary stack: `pytest` with `pytest-asyncio`; prefer `httpx.ASGITransport` clients for API paths.
- File naming `tests/test_<module>.py`; test functions start with `test_`. Group feature-specific cases under subpackages (e.g., `tests/auth/`).
- Spin up the suite via `make test`; target a case with `pytest tests/auth/test_router.py::test_login_returns_token_for_valid_credentials`.

## Commit & Pull Request Guidelines
- Follow Conventional Commits (`feat(auth): add login tests`); keep messages imperative and scoped.
- PRs should outline motivation, linked issues, local verification commands (`make all`, `make test`), and include curl examples or screenshots for API-facing changes.

## Security & Configuration Tips
- Store secrets in `.env`; ensure values align with `src/config.py` defaults and compose environment variables (`DB_DSN`, `SQLITE_PATH`).
- Run `make all` plus a manual API smoke test (curl `/health`) before merging to avoid runtime regressions.
