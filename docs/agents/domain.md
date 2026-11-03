# Domain docs

This repo has a single context:

- `GLOSSARY.md` (repo root): the canonical name and one-line meaning of every domain term. Read it before naming anything; use its terms in code, issues and PRs, and avoid the words under each `_Avoid_`.
- `docs/adr/`: architecture decision records, numbered `NNNN-slug.md`.

## Keeping them current

- When a ticket introduces or sharpens a domain concept, update `GLOSSARY.md` in the same PR. Keep it a glossary: definitions only, no implementation detail.
- Write an ADR only for a decision that is hard to reverse, would surprise a future reader, and came from a real trade-off. One paragraph is enough.
- When code contradicts the glossary or an ADR, raise it in the PR rather than silently picking one.
