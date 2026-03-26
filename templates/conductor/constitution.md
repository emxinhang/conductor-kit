# Constitution — {{PROJECT_NAME}}

> **Non-negotiable architectural invariants.**
> `/planner-track` MUST check this before finalizing any `IMPLEMENTATION_PLAN.md`.
> `/review-plan` uses this as a gate before implementation starts.

---

## Plan Author Checklist

Before approving a plan, confirm all of the following:

- [ ] All Backend Invariants respected
- [ ] All Frontend Invariants respected
- [ ] No new dependencies added without explicit decision
- [ ] Migration strategy documented if DB schema changes
- [ ] Security requirements satisfied
- [ ] Race conditions considered (concurrent write paths)

---

## Backend Invariants

| Rule | Why |
|------|-----|
| {{rule}} | {{reason}} |

---

## Frontend Invariants

| Rule | Why |
|------|-----|
| {{rule}} | {{reason}} |

---

## Security Requirements

- All user input validated at API boundary
- Auth required on all mutating endpoints
- No sensitive data in localStorage
- No raw SQL string interpolation

---

## Quality Gates (non-negotiable)

- **NEVER** auto-commit or auto-push — user tests locally first
- Read files before modifying — no blind edits
- Verify (lint + build + smoke) before claiming done

---

## Locked Tech Decisions

| Area | Choice | Rationale |
|------|--------|-----------|
| {{area}} | {{choice}} | {{rationale}} |

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| {{TODAY}} | Initial constitution | CS |
