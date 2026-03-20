# General Code Style Guide

Applies across all languages and agents (CS · AG · CD).

## Core Principles

1. **Readability first** — Code is read 10x more than written. Optimize for the next reader.
2. **Consistency** — Follow existing patterns in the file before introducing new ones.
3. **Simplicity** — The minimum complexity that solves the problem. No speculative abstractions.
4. **Verification before completion** — Never claim done without evidence (logs, build output, test pass).
5. **Explicitness** — Prefer explicit over implicit. Name things for what they do, not what they are.

## Naming

- Names describe **purpose**, not type. `user_id` not `id_str`.
- Booleans: `is_`, `has_`, `can_`, `should_` prefix.
- Functions: verb phrases — `get_user`, `validate_payload`, `send_email`.
- Avoid abbreviations unless universal (`id`, `url`, `db`, `ctx`).

## File & Module Organization

- One responsibility per file.
- Group by feature, not by type. `users/` not `models/ + routes/ + services/`.
- Keep files under 300 lines. If longer, split by responsibility.

## Comments

- Comment **why**, not **what**. Code explains what; comments explain intent.
- Do not comment out dead code — delete it. Git remembers.
- Mark unresolved issues: `# TODO(AG): ...` or `// TODO(CS): ...`

## Error Handling

- Validate at system boundaries (user input, external APIs). Trust internal code.
- Fail fast and loudly in dev. Graceful degradation only in user-facing paths.
- Never swallow exceptions silently (`except: pass` / `catch(e) {}`).

## Commits

- Commit message format: `type(scope): short description`
- Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`
- One logical change per commit. Do not bundle unrelated changes.
- Never commit commented-out code, debug prints, or hardcoded secrets.

## Zero-Loop Verification

Before marking any task done:

```
1. Run the build / lint / type-check
2. Run relevant tests or manual smoke test
3. Confirm output is green
4. Then mark [x] in plan.md
```

Never report completion without step 3 evidence.
