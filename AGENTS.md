# Phoenix Agent Guidelines

This document provides conventions for agentic coding assistants.

## Python (root)

- **Lint & Format**: `ruff check . --fix`, `ruff format .`
- **Test**: `pytest`
- **Run a single test**: `pytest tests/unit/phoenix/test_file.py`
- **Type Check**: `mypy`

## Frontend (`app` directory)

- **Install**: `pnpm install`
- **Lint & Format**: `pnpm lint:fix`, `pnpm prettier`
- **Test**: `pnpm test`
- **Run a single test**: `pnpm test src/components/test_component.spec.ts`
- **Build**: `pnpm build`

## Code Style

- **Imports**: Use `ruff` for Python import sorting. Use `eslint-plugin-simple-import-sort` for TS/JS.
- **Formatting**: Adhere to `ruff` and `prettier` configurations.
- **Types**: Add types for all new code.
- **Naming**: Follow existing conventions in the surrounding code.
- **Error Handling**: Use `try/except` in Python and `try/catch` in TypeScript for error handling.
