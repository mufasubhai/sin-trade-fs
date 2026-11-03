## Package managers

- Frontend (`sin-trade-fe`): use `pnpm`; commit only `pnpm-lock.yaml`, never a `package-lock.json`.
- Backend and data science: each service has its own venv (`sin-trade-be/be-venv`, `sin-trade-ds/ds-venv`) installed from its `requirements.txt`.

## Supabase migrations

Since 2026-10-30 Supabase gives new tables no Data API access by default, so every migration that creates a table in `public` also grants access to the role that queries it:

- Tables the backend reads as the signed-in user (profiles, Watched Assets, Targets): `grant ... to authenticated;`
- Tables only the services touch (`ml_*`, price data): `grant ... to service_role;`

Grant to `authenticated` or `service_role` only; every table holds per-user or internal data, so `anon` gets no grants. Every table has RLS enabled with a policy, and RLS decides which rows a user sees. Adding a column to an existing table needs no new grant.

## Checks

Run the checks for every service a ticket touches:

- `sin-trade-fe`: `pnpm test`, `pnpm typecheck`, `pnpm lint`, `pnpm build`
- `sin-trade-be` / `sin-trade-ds`: `pytest` inside that service's venv (see CLAUDE.md)

## Git workflow

`main` is production. `dev` is the integration branch. Never commit directly to either.

For each ticket:

1. Create a new feature branch from an up-to-date `dev`: `git switch dev && git pull && git switch -c <issue-number>-<short-slug>` (e.g. `12-signal-correctness`).
2. When the ticket is implemented and the checks pass, stage the changes (`git add`) and stop for Adrian's local review. Summarise what's staged, and list any migration Adrian must run by hand in the Supabase SQL Editor before the code can reach `main`. The commit waits for Adrian's go-ahead.
3. Once Adrian approves, commit to the branch, referencing the issue (`Refs #<n>`), push, and open a PR into `dev`: `gh pr create --base dev`. Fill out every applicable section of `.github/pull_request_template.md` as the PR body (including `Closes #<n>`), and tick only the checklist items you actually verified.
4. After opening the PR, post a single-line, file-level review comment on **every** changed file, explaining what changed in that file and why. Use: `gh api repos/{owner}/{repo}/pulls/<pr>/comments -f commit_id=<head sha> -f path=<file> -f subject_type=file -f body='<one line>'`. Re-comment on any file whose changes are materially revised by later commits.
5. Leave merging to Adrian. Adrian batches tickets from `dev` into `main` (production); agents never open PRs into `main`.

## Agent skills

### Issue tracker

Issues and specs are tracked in GitHub Issues on mufasubhai/sin-trade-fs via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Design Principles

- **YAGNI**: Don't build it until you need it.
- **DRY**: Extract patterns after second duplication, not before.
- **Fail Fast**: Explicit errors beat silent failures.
- **Simple First**: Write the obvious solution, optimize only if needed.
- **Delete Aggressively**: Less code = fewer bugs.
- **Semantic Naming**: Always name variables, parameters, and API endpoints with verbose, self-documenting names that optimize for comprehension by both humans and LLMs, not brevity (e.g., `waitUntilObjectIsSaved = true` vs `wait = true`).
- **Glossary names**: name code after the `GLOSSARY.md` term for the concept (`watched_asset`, `tracked_asset`, `signal`), and rename legacy names (`user_assets`, `active_assets`) when a ticket touches them.
