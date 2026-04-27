# Tasks: {{FEATURE_NAME}} (Track {{TRACK_ID}})

> **Spec**: [spec.md](./spec.md) | **Plan**: [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md)
> **Author**: CS | **Date**: {{DATE}}

---

## Task Granularity Rule

**Mỗi task phải hoàn thành trong ≤ 5 phút.** Nếu estimate > 5 phút → bắt buộc chia nhỏ thành sub-tasks trước khi bắt đầu code. Task quá lớn = context drift, khó review, khó rollback.

Checklist trước khi lock plan:
- [ ] Mỗi task có exactly 1 file target hoặc 1 action rõ ràng
- [ ] Task có verification step cụ thể (không phải "check xem ổn không")
- [ ] Không có task nào kiểu "implement feature X" — phải là "create file Y với function Z"

---

## Legend

| Marker | Meaning |
|--------|---------|
| `[P]` | Parallel-safe — can run on AG + CD simultaneously (no shared file writes) |
| `[SEQ]` | Sequential — depends on a prior task |
| `[US1]` | Traces to User Story 1 in spec.md |
| `[CHK]` | Checkpoint — ATu must verify before continuing |

---

## Phase 1 — Backend

### [US1] Data Layer

- [ ] `[P]` Create model: `backend/app/models/{{model}}.py`
- [ ] `[P]` Create schema: `backend/app/schemas/{{schema}}.py`
- [ ] `[SEQ]` Create migration: `alembic revision --autogenerate -m "add_{{table}}"`

**[CHK-1]** `alembic upgrade head` clean → table exists in DB

### [US1] Service + API

- [ ] `[P]` Create service: `backend/app/services/{{service}}.py`
- [ ] `[P]` Create router: `backend/app/api/v1/{{router}}.py`
- [ ] `[SEQ]` Register router in `backend/app/main.py`

**[CHK-2]** `curl http://localhost:8000/api/v1/{{endpoint}}` → 200

---

## Phase 2 — Frontend

### [US1] API Integration

- [ ] `[P]` Add types + fetch functions: `frontend/src/api/{{module}}.ts`

### [US2] UI Components

- [ ] `[P]` Create component: `frontend/src/features/{{module}}/components/{{Component}}.tsx`
- [ ] `[P]` Create page: `frontend/src/features/{{module}}/pages/{{Page}}.tsx`
- [ ] `[SEQ]` Add route in `frontend/src/lib/navigation.ts`

**[CHK-3]** Page renders → `npm run build` clean, no TS errors

---

## Phase 3 — QA

### Acceptance Criteria (from spec.md)

- [ ] SC-001 passes: {{description}}
- [ ] SC-010 passes: {{description}}

### Wrap-up

- [ ] No console errors
- [ ] `python conductor/status.py transition {{track-id}} qa CS "ready for QA"`
