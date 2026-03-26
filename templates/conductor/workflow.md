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

- `📅 Planned`: da co PRD/spec (+ spec.md structured)
- `[📅 Planned]`: da co `IMPLEMENTATION_PLAN.md` + `tasks.md`
- `[💻 Dev]`: dang code
- `[🧪 QA]`: dang verify, smoke test, handoff
- `[✅ Completed]`: da release va wrap-up

## Track Artifacts

Each track folder `conductor/tracks/<id>/` should contain:

| File | Created by | Required |
|------|-----------|---------|
| `PRD.md` | `/brainstorm-track` | Yes |
| `spec.md` | `/brainstorm-track` | Yes — use `conductor/track-templates/SPEC_TEMPLATE.md` |
| `IMPLEMENTATION_PLAN.md` | `/planner-track` | Yes |
| `tasks.md` | `/planner-track` | Yes — use `conductor/track-templates/TASKS_TEMPLATE.md` |
| `CHANGELOG.md` | auto via `status.py transition` | Yes |
| `SESSION.md` | AG/CD on pause | When paused |

## Constitution Gate

`conductor/constitution.md` contains non-negotiable architectural invariants.

- `/brainstorm-track` checks constitution before finalizing spec.md
- `/planner-track` checks constitution before approving IMPLEMENTATION_PLAN.md
- If plan violates constitution → flag to user, do not proceed

## Session Flow

1. Session start:
   - `python conductor/status.py` — xem toàn bộ tình hình ngay
   - Read `conductor/state.md` — ACTIVE track, PIPELINE queue
   - Read `docs/memory/MEMORY.md` (index)
   - Read `docs/memory/00_active_context.md`
   - **CS**: Read `docs/memory/session_save_cs.md` nếu tồn tại
   - **AG/CD**: Read `conductor/tracks/[active-track]/SESSION.md` nếu tồn tại
2. Planning (CS):
   - Read `PRD.md` / `spec.md`
   - Create or update `IMPLEMENTATION_PLAN.md`
   - Move track `📅 Planned -> [📅 Planned]` trong `tracks.md`
   - Update `conductor/state.md` PIPELINE khi plan xong
3. Development (AG hoặc CD):
   - Move `[📅 Planned] -> [💻 Dev]`; update `state.md` ACTIVE
   - Write `CHANGELOG.md` whenever status changes
   - Khi pause: ghi `conductor/tracks/[id]/SESSION.md`
4. QA:
   - After verification and smoke test, move `[💻 Dev] -> [🧪 QA]`
5. Release and wrap-up:
   - After release, move `[🧪 QA] -> [✅ Completed]`
   - `python conductor/status.py done` — promote PIPELINE[0] lên ACTIVE
   - Save learnings vào `docs/memory/`
   - Xóa `SESSION.md` của track vừa complete

## Memory Rules

- Load memory by context profile instead of loading everything
- Store learnings only in `docs/memory/`
- Use `docs/memory/session_save.md` as the resumable session checkpoint
- Prune low-value memory when files become too large

## Auto-Update Board (status.py transition)

Mỗi workflow transition phải chạy lệnh atomic sau — cập nhật đồng thời `tracks.md` + `state.md` + `CHANGELOG.md`:

```bash
python conductor/status.py transition <track-id> <phase> [agent] [note]
```

| Phase | Trigger | Agent |
|-------|---------|-------|
| `planned` | `/planner-track` hoàn thành | CS |
| `dev` | `/handoff` bắt đầu | AG/CD |
| `qa` | Backend verify pass (zero-loop-dev) | AG/CD |
| `done` | `/deploy-track` smoke test pass | AG/CS |

Sau khi `done`, luôn chạy thêm `python conductor/status.py done` để promote PIPELINE → ACTIVE.

## Ownership

- `/conductor` owns track status transitions
- `/update-knowledge` may append ledger and session state during wrap-up

## Definition of Done

- Code da verify theo quy trinh hien hanh
- Track status da cap nhat dung state machine
- `CHANGELOG.md` da ghi transition neu co doi status
- Memory/session da duoc cap nhat qua `docs/memory/`
