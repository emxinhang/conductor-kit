# Conductor Workflow

This file is the canonical workflow reference for the repository.

## Reference Roots

- Workflow reference: `conductor/workflow.md`
- Shared docs root: `docs/`
- Memory index: `docs/memory/MEMORY.md`

## Core Rules

- Use `conductor/tracks.md` as the track status master list
- Use `docs/memory/` as the only persistent memory storage area
- Keep `.agent`, `.claude`, and `.codex` aligned to this file instead of maintaining separate workflow rules

## Track State Machine

`📅 Planned -> [📅 Planned] -> [💻 Dev] -> [🧪 QA] -> [✅ Completed]`

- `📅 Planned`: da co PRD/spec
- `[📅 Planned]`: da co `IMPLEMENTATION_PLAN.md`
- `[💻 Dev]`: dang code
- `[🧪 QA]`: dang verify, smoke test, handoff
- `[✅ Completed]`: da release va wrap-up

## Session Flow

1. Session start:
   - Read `docs/memory/MEMORY.md`
   - Read `docs/memory/00_active_context.md`
   - Read `conductor/tracks.md`
   - Read `docs/memory/session_save.md` if it exists
2. Planning:
   - Read `PRD.md` / `spec.md`
   - Create or update `IMPLEMENTATION_PLAN.md`
   - Move track `📅 Planned -> [📅 Planned]`
3. Development:
   - When coding starts, move `[📅 Planned] -> [💻 Dev]`
   - Write `CHANGELOG.md` whenever status changes
4. QA:
   - After verification and smoke test, move `[💻 Dev] -> [🧪 QA]`
5. Release and wrap-up:
   - After release and session wrap-up, move `[🧪 QA] -> [✅ Completed]`
   - Save learnings and latest session state into `docs/memory/`

## Memory Rules

- Load memory by context profile instead of loading everything
- Store learnings only in `docs/memory/`
- Use `docs/memory/session_save.md` as the resumable session checkpoint
- Prune low-value memory when files become too large

## Ownership

- `/conductor` owns track status transitions
- `/update-knowledge` may append ledger and session state during wrap-up

## Definition of Done

- Code da verify theo quy trinh hien hanh
- Track status da cap nhat dung state machine
- `CHANGELOG.md` da ghi transition neu co doi status
- Memory/session da duoc cap nhat qua `docs/memory/`
