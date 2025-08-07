Agent guide for phoenix-mango (build/test/style, ~20 lines)

- Python (root): lint/format with `uv tool run ruff format && uv tool run ruff check --fix`; type-check with `mypy --strict`; run unit tests `pytest tests/unit -q`; single test `pytest tests/unit/<path>/test_file.py::test_name -q`.
- Python via tox (preferred CI parity): unit `tox -e unit_tests -- tests/unit`; single `tox -e unit_tests -- tests/unit/<path>/test_file.py::test_name`; integration `tox -e integration_tests`; type-check `tox -e type_check`.
- Python style: Ruff line-length 100; import order via Ruff/isort; strict typing (mypy plugins: strawberry, pydantic); avoid bare except, raise specific errors, prefer explicit returns; doctests enabled.
- JS/TS app (app/): install `pnpm i`; build `pnpm build` (relay then Vite); dev `pnpm dev`; lint `pnpm lint` / fix `pnpm lint:fix`; format `pnpm prettier` or check `pnpm prettier:check`; type-check `pnpm typecheck`.
- App tests: unit `pnpm test` (Vitest); watch `pnpm test:watch`; single test `pnpm test -- src/<path>.test.tsx -t "name or pattern"`; e2e `pnpm test:e2e` (Playwright) or UI `pnpm test:e2e:ui`.
- JS monorepo (js/): build all `pnpm -C js run build`; lint `pnpm -C js run lint`; type-check `pnpm -C js run type:check`.
- JS/TS style (app/.eslintrc.js): React, hooks rules on; no `console`; unused vars allowed only if prefixed `_`; import order via `simple-import-sort` with groups (react, @*, @phoenix, side-effects, parent, relative, styles).
- App TypeScript (tsconfig): strict true; moduleResolution bundler; path alias `@phoenix/*`; prefer sorted import suggestions plugin.
- Prettier (app): trailingComma es5.
- Pre-commit: `pre-commit run -a` (Ruff format+lint, nbqa for notebooks, Prettier, ESLint); hook forbids committing on local `main`.
- Cursor rules (app/.cursor): Organization: reusable components in `src/components`; stories in `stories/`.
- Cursor rules (styling): use Emotion for CSS; prefer design tokens/vars from `src/GlobalStyles.tsx`; use data-attributes; local CSS vars; suffix style vars with `CSS`.
- Cursor rules (stories): define comprehensive variants; add controls; use docstrings.
- Cursor rules (charting): use Recharts; apply `src/components/chart/defaults.tsx`; keep chart colors semantic in `src/GlobalStyles.tsx`.
- Cursor rules (js packages client): API methods namespaced (`prompts`, `experiments`, `projects`); use object params (`getPrompt({ promptIdentifier })`); verbs: get/create/list/add/delete; bulk: `log*`.
- Python pytest defaults: asyncio auto; import-mode importlib; show locals; new-first; coverage config present.
- Engines/tooling: Node >=22 for app; pnpm enforced; Python >=3.9,<3.14; use `uv` tooling in tox/tasks.
