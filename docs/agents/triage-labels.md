# Triage labels

Each open issue carries exactly one triage label:

| Label | Meaning |
|---|---|
| `needs-triage` | New; Adrian has not evaluated it yet. |
| `needs-info` | Blocked on information or an action from someone; the body says what it is waiting on. |
| `ready-for-agent` | Fully specified; an agent can implement it once its `Blocked by` issues are closed. |
| `ready-for-human` | Only a human can do it (dashboards, credentials, manual migrations). |
| `wontfix` | Decided against; close the issue with a one-line reason. |

When an agent finds an issue under-specified, it comments with the open questions and moves it to `needs-info`.
