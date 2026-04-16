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

`ðŸ“… Planned -> [ðŸ“… Planned] -> [ðŸ’» Dev] -> [ðŸ§ª QA] -> [âœ… Completed]`

- `ðŸ“… Planned`: da co PRD/spec (+ spec.md structured)
- `[ðŸ“… Planned]`: da co `IMPLEMENTATION_PLAN.md` + `tasks.md`
- `[ðŸ’» Dev]`: dang code
- `[ðŸ§ª QA]`: dang verify, smoke test, handoff
- `[âœ… Completed]`: da release va wrap-up

## Track Artifacts

Each track folder `conductor/tracks/<id>/` should contain:

| File | Created by | Required |
|------|-----------|---------|
| `PRD.md` | `/brainstorm-track` | Yes |
| `spec.md` | `/brainstorm-track` | Yes â€” use `conductor/track-templates/SPEC_TEMPLATE.md` |
| `contract_delta.md` | `/brainstorm-track` (track 014+) | Yes if API/DB changes |
| `IMPLEMENTATION_PLAN.md` | `/planner-track` | Yes |
| `tasks.md` | `/planner-track` | Yes â€” use `conductor/track-templates/TASKS_TEMPLATE.md` |
| `CHANGELOG.md` | auto via `status.py transition` | Yes |
| `SESSION.md` | AG/CD on pause | When paused |

## Contract-First Workflow (track 014+)

See full framework: `docs/contracts/FRAMEWORK.md`

**Quick reference per phase**:

| Phase | Contract action |
|-------|----------------|
| `brainstorm-track` | Draft `contract_delta.md` — list endpoints/schema changes |
| `planner-track` | Update `docs/contracts/api/ha_lac.yaml`, run `make sync-types` |
| Dev | Backend implements spec; frontend uses generated types |
| `done-checklist` | Gate: contract updated + types synced + `_registry.md` bumped |

## Constitution Gate

`conductor/constitution.md` contains non-negotiable architectural invariants.

- `/brainstorm-track` checks constitution before finalizing spec.md
- `/planner-track` checks constitution before approving IMPLEMENTATION_PLAN.md
- If plan violates constitution â†’ flag to user, do not proceed

## Session Flow

1. Session start:
   - `python conductor/status.py` â€” xem toÃ n bá»™ tÃ¬nh hÃ¬nh ngay
   - Read `conductor/state.md` â€” ACTIVE track, PIPELINE queue
   - Read `docs/memory/MEMORY.md` (index)
   - Read `docs/memory/00_active_context.md`
   - **CS**: Read `docs/memory/session_save_cs.md` náº¿u tá»“n táº¡i
   - **AG/CD**: Read `conductor/tracks/[active-track]/SESSION.md` náº¿u tá»“n táº¡i
2. Planning (CS):
   - Read `PRD.md` / `spec.md`
   - Create or update `IMPLEMENTATION_PLAN.md`
   - Move track `ðŸ“… Planned -> [ðŸ“… Planned]` trong `tracks.md`
   - Update `conductor/state.md` PIPELINE khi plan xong
3. Development (AG hoáº·c CD):
   - Move `[ðŸ“… Planned] -> [ðŸ’» Dev]`; update `state.md` ACTIVE
   - Write `CHANGELOG.md` whenever status changes
   - Khi pause: ghi `conductor/tracks/[id]/SESSION.md`
4. QA:
   - After verification and smoke test, move `[ðŸ’» Dev] -> [ðŸ§ª QA]`
5. Release and wrap-up:
   - After release, move `[ðŸ§ª QA] -> [âœ… Completed]`
   - `python conductor/status.py done` â€” promote PIPELINE[0] lÃªn ACTIVE
   - Save learnings vÃ o `docs/memory/`
   - XÃ³a `SESSION.md` cá»§a track vá»«a complete

## Memory Rules

- Load memory by context profile instead of loading everything
- Store learnings only in `docs/memory/`
- Use `docs/memory/session_save.md` as the resumable session checkpoint
- Prune low-value memory when files become too large

## Auto-Update Board (status.py transition)

Má»—i workflow transition pháº£i cháº¡y lá»‡nh atomic sau â€” cáº­p nháº­t Ä‘á»“ng thá»i `tracks.md` + `state.md` + `CHANGELOG.md`:

```bash
python conductor/status.py transition <track-id> <phase> [agent] [note]
```

| Phase | Trigger | Agent |
|-------|---------|-------|
| `planned` | `/planner-track` hoÃ n thÃ nh | CS |
| `dev` | `/handoff` báº¯t Ä‘áº§u | AG/CD |
| `qa` | Backend verify pass (zero-loop-dev) | AG/CD |
| `done` | `/deploy-track` smoke test pass | AG/CS |

Sau khi `done`, luÃ´n cháº¡y thÃªm `python conductor/status.py done` Ä‘á»ƒ promote PIPELINE â†’ ACTIVE.

## Ownership

- `/conductor` owns track status transitions
- `/update-knowledge` may append ledger and session state during wrap-up

## Definition of Done

- Code da verify theo quy trinh hien hanh
- Track status da cap nhat dung state machine
- `CHANGELOG.md` da ghi transition neu co doi status
- Memory/session da duoc cap nhat qua `docs/memory/`

