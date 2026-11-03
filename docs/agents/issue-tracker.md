# Issue tracker

Issues live in GitHub Issues on `mufasubhai/sin-trade-fs`. Use the `gh` CLI for everything (`gh issue list`, `gh issue view <n>`, `gh issue create`).

## Milestones

Every issue belongs to one milestone, worked in this order:

1. **Fixes**: bugs, security and reliability in the existing pipeline
2. **Feature improvements**: improvements to existing features
3. **UI**: UI and UX improvements
4. **New features**

## Writing an issue

- Title names the outcome, using `GLOSSARY.md` terms.
- Body: the problem with `file:line` references, the agreed behaviour, and acceptance criteria.
- Dependencies are written as `Blocked by #<n>` near the top.
- Apply one triage label (see `triage-labels.md`) and a type label (`bug`, `enhancement`, `documentation`).

## Picking up an issue

Take issues labelled `ready-for-agent` whose `Blocked by` issues are closed, lowest milestone first. Follow the Git workflow in `AGENTS.md`.
