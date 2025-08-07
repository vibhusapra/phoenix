# Phoenix Codebase Guide for AI Agents

## Build/Test Commands
**Python (root):**
- Test: `pytest tests/` or `pytest tests/path/to/test.py::TestClass::test_method`
- Lint: `ruff check . --fix` and `ruff format .`
- Type check: `mypy --strict src/`
- Pre-commit: `pre-commit run --all-files`

**TypeScript/React (app/):**
- Build: `cd app && pnpm run build`
- Test: `cd app && pnpm test` or `vitest run path/to/test.spec.ts`
- Lint: `cd app && pnpm lint`
- Type check: `cd app && pnpm typecheck`

## Code Style
- **Python**: Follow ruff config (line-length: 100, target: py39+), use type hints
- **TypeScript**: Use emotion for CSS styling, design tokens from GlobalStyles.tsx
- **Imports**: Single-line imports, sorted by ruff/eslint
- **Components**: Reusable components in src/components, stories in stories/
- **Error handling**: Use proper exception types, async/await patterns
- **Naming**: snake_case (Python), camelCase (TS/JS), PascalCase (React components)