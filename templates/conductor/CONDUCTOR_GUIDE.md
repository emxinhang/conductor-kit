# Conductor Guide — [[PROJECT_NAME]]
> Hướng dẫn vận hành hệ thống điều phối 3 agents: CS · AG · CD

---

## Agents

| Agent | Tool | Role |
|---|---|---|
| **CS** | Claude Sonnet | Orchestrator — brainstorm, plan, review, merge |
| **AG** | Gemini | Implementer — code backend/frontend theo plan |
| **CD** | Codex | Implementer — code, debug, alternative to AG |

**Quy tắc cuốn chiếu**: 1 implementation track tại 1 thời điểm. AG và CD không chạy song song (conflict risk cao trên monorepo).

---

## Xem tình hình ngay

```bash
python conductor/status.py
```

Dashboard hiển thị: ai đang làm gì, pipeline queue, done gần đây.

---

## Files quan trọng

| File | Mục đích | Ai đọc/ghi |
|---|---|---|
| `conductor/state.md` | Shared orchestration state | Tất cả agents — đọc đầu tiên |
| `conductor/tracks.md` | Master list tất cả tracks | CS cập nhật status |
| `conductor/workflow.md` | Canonical workflow reference | Tất cả agents |
| `docs/memory/session_save_cs.md` | CS planning context | CS only |
| `conductor/tracks/[id]/SESSION.md` | Track implementation context | AG/CD — agent-agnostic |

---

## Session flow — CS (plan/orchestrate)

```
1. python conductor/status.py
2. Read conductor/state.md
3. Read docs/memory/session_save_cs.md  (nếu có)
4. Làm việc: brainstorm → plan → review → update PIPELINE trong state.md
5. /update-knowledge → ghi session_save_cs.md
```

## Session flow — AG hoặc CD (implement)

```
1. python conductor/status.py
2. Read conductor/state.md  →  xem ACTIVE track
3. Read conductor/tracks/[active-track]/SESSION.md  (nếu có — pick up từ session trước)
4. Implement theo IMPLEMENTATION_PLAN.md
5. Khi pause: ghi SESSION.md vào track folder
6. Khi done: python conductor/status.py done
```

---

## Lệnh status.py

```bash
python conductor/status.py              # Dashboard
python conductor/status.py done         # Mark ACTIVE done, promote PIPELINE[0]
python conductor/status.py note "..."   # Cập nhật notes của ACTIVE track
python conductor/status.py add "name"   # Thêm vào BACKLOG
```

---

## Track lifecycle

```
📅 Planned  →  [📅 Planned]  →  [💻 Dev]  →  [🧪 QA]  →  ✅ Completed
    PRD          IMPL_PLAN       Coding       Verify       Released
    (CS plan)    (CS review)     (AG/CD)      (ATu test)
```

**state.md mapping:**
- `📅 Planned` + `[📅 Planned]` → UPCOMING / PIPELINE
- `[💻 Dev]` → ACTIVE
- `✅ Completed` → DONE

---

## Session save — quy tắc

**CS** ghi vào `docs/memory/session_save_cs.md`:
- Planning dở dang, decisions cần nhớ, next steps

**AG/CD** ghi vào `conductor/tracks/[id]/SESSION.md`:
- Code đến đâu, file nào đang mở, next step cụ thể
- Agent-agnostic: AG save → CD có thể pick up, và ngược lại
- Xóa file này khi track complete

**Không dùng** `docs/memory/session_save.md` (deprecated).

---

## Prompt mẫu khi mở session mới

### CS
```
Read conductor/state.md first. Then read docs/memory/session_save_cs.md.
Your role: plan/review tracks in PIPELINE or upcoming.
Do NOT touch implementation files.
Update PIPELINE in state.md when plan is done.
```

### AG hoặc CD
```
Read conductor/state.md first.
Your track: [track-name từ ACTIVE slot].
Read conductor/tracks/[track-id]/SESSION.md for context.
Implement only files related to this track.
Update SESSION.md when you pause or finish.
When done: python conductor/status.py done
```

---

## Khi nào update state.md

| Event | Action |
|---|---|
| CS xong plan một track | Thêm track vào PIPELINE |
| AG/CD bắt đầu implement | Update ACTIVE (track, agent, phase, started) |
| AG/CD pause | Update ACTIVE notes |
| Track done | `status.py done` (auto-promote) |
