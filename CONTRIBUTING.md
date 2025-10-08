# Contributing

Before making changes to this repository, first discuss with the repository owners what you intend to do.

## Setting up your development environment

1. Please refer to the [AGENTS.md](AGENTS.md) file for detailed contribution guidelines.
2. Setup your development environment:

```bash
uv venv
source venv/bin/activate
uv sync --upgrade --dev
```

3.  Install the git hook scripts:

```bash
pre-commit install
```

4.  Ensure code quality before committing:

```bash
make all
```

## Testing

Run the entire test suite with the provided make target:

```bash
make test
```

Target a specific module (or directory) by passing it to `TESTS`:

```bash
make test TESTS=tests/auth/test_router.py
```

Execute an individual test or use pytest modifiers:

```bash
make test TESTS=tests/auth/test_router.py::test_login_returns_token_for_valid_credentials
make test PYTEST_ARGS="-k login"
```
