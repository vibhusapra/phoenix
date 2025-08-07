AGENTS quickstart for Phoenix (Python + TS)

Build/Lint/Test
- Python (requires uv): install deps: uv pip install --strict -r requirements/dev.txt
- Python lint/format: uvx ruff format && uvx ruff check --fix; types: uv run mypy --strict src/phoenix
- Python tests: uv run pytest tests; single: uv run pytest tests/unit/test_file.py::test_name -k "expr"
- UI app/ (Node>=22, pnpm): pnpm i; build: pnpm build; type: pnpm typecheck; lint: pnpm lint | pnpm lint:fix; prettier: pnpm prettier:check
- UI tests: unit: pnpm test or pnpm test src/path.test.tsx -t "name"; e2e: pnpm test:e2e; single e2e: pnpm test:e2e -g "title"
- JS monorepo js/: install at root: pnpm i; build all: pnpm -C js build; lint: pnpm -C js lint; type: pnpm -C js type:check; per-package tests: pnpm -C js -r test

Code style (Python)
- Formatting/lint via ruff (line length 100); imports sorted by ruff-isort; run ruff format then ruff check --fix
- Strict typing via mypy (plugins: strawberry, pydantic); add annotations everywhere; avoid Any; prefer TypedDict/Protocol/Annotated as needed
- PEP8 naming: snake_case for functions/vars, PascalCase for classes, UPPER_CASE for constants; keep functions small; avoid side-effects at import
- Errors: raise specific exceptions; never bare except; log with logging not print; validate inputs with pydantic where applicable

Code style (TypeScript/React)
- ESLint enforced: no console; react-hooks rules on; react-compiler rule on; simple-import-sort with groups (react/@emotion, @arizeai, @phoenix, side-effects, parent, relative, styles)
- Imports: prefer @phoenix/components over deprecated @arizeai/components APIs (see deprecate rules in app/.eslintrc.js)
- Formatting via Prettier (app/.prettierrc.json); keep types explicit; avoid any; favor zod schemas
- Styling: use emotion; follow design tokens/vars in app/src/GlobalStyles.tsx; style variants via data attributes; name style vars with CSS suffix

Cursor rules to follow
- app/.cursor/rules: organization (components in src/components; stories in stories/), stories (variants, controls, docstrings), styling (emotion, tokens), charting (recharts with defaults)
- packages/phoenix-client/.cursor/rules/general.mdc: Python client API: light deps, namespaced methods, kwargs-only, verb prefixes (get/create/list/add/delete/log), pandas helpers
- js/packages/phoenix-client/.cursor/rules/general.mdc: TS client API: object params, same verb prefixes

Repo hygiene
- Use pre-commit: ruff, prettier, eslint; don’t commit to local main; prefer pnpm (enforced by only-allow)