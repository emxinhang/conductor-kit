# Constitution — TMS-2026

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

### FastAPI / SQLAlchemy

| Rule | Why |
|------|-----|
| `response_model=Schema` REQUIRED on every router | `@computed_field` silently breaks without it |
| `selectinload()` REQUIRED for all nested relations | `MissingGreenlet` in async context otherwise |
| All service functions must be `async` | Blocking calls in async context causes event loop stall |
| No raw SQL string interpolation | SQL injection risk — use SQLAlchemy ORM only |
| NEVER use `async with db.begin()` inside a service method | `flush()` already begins implicit transaction — calling `begin()` again raises `InvalidRequestError`. Use `try/except` + explicit `await db.rollback(); raise` instead |
| Mass-assignment via `setattr` MUST use explicit whitelist | `hasattr()` allows any column to be overwritten — use `ALLOWED_FIELDS = {...}` set |

### Datetime

| Rule | Why |
|------|-----|
| `@field_serializer` must append `'Z'` to all datetime fields | Frontend gets +7h timezone bug without it |

### File Storage (Cloudflare R2)

| Rule | Why |
|------|-----|
| Store `object_key` WITHOUT bucket prefix in DB | Double-prefix 404 on presigned URL generation |
| Generate presigned URL at read time via `@computed_field` | Never store full URLs in DB — they expire |

### Migrations

| Rule | Why |
|------|-----|
| New migration file MUST be git committed before Railway deploy | Railway reads committed files only |
| Always `alembic upgrade head` locally before claiming migration done | Verify on real DB, not just generate |

---

## Frontend Invariants

### State / Data

| Rule | Why |
|------|-----|
| `useState(initialData)` won't re-sync when prop changes | Add `useEffect(() => setState(initialData), [initialData])` |
| `useShallow` REQUIRED when selecting arrays/objects from Zustand | Array ref changes every render → infinite re-render loop |
| Global hotkeys must check `document.activeElement` first | Triggers inside input fields otherwise |

### Architecture

| Rule | Why |
|------|-----|
| Feature folder: `frontend/src/features/{module}/` | Module isolation — don't cross-import between features |
| API layer: `frontend/src/api/{module}.ts` | Single source of truth for types + fetch fns |
| Routing: TanStack Router via `frontend/src/lib/navigation.ts` | Project standard — no ad-hoc `window.location` |
| UI: MUI v7 | Locked in — don't introduce Chakra/shadcn/etc. |

### Build

| Rule | Why |
|------|-----|
| `npm run build` must pass before claiming frontend done | TS errors only surface at build time |
| Vite cache issues → delete `node_modules/.vite`, restart | Stale cache causes phantom errors |

---

## Security Requirements

- All user input validated at API boundary (Pydantic schemas)
- Auth: every mutating endpoint requires `current_user` dependency
- RBAC: department permission check on sensitive resources
- No sensitive data in `localStorage` (sessions, tokens)
- No raw SQL string interpolation anywhere

---

## Quality Gates (non-negotiable)

- **NEVER** auto-commit or auto-push — ATu tests locally first
- Read files before modifying — no blind edits
- Verify (lint + build + smoke) before claiming done
- Migrations committed before Railway deploy

---

## Locked Tech Decisions

| Area | Choice | Rationale |
|------|--------|-----------|
| Backend framework | FastAPI (Python 3.11+) | Locked |
| Database | PostgreSQL 16 | Locked |
| ORM | SQLAlchemy 2.x async | Locked |
| Frontend framework | React 19 + Vite | Locked |
| UI library | shadcn/ui + Tailwind CSS v4 | Locked |
| Routing | React Router DOM v7 | Locked |
| State (server) | TanStack Query | Locked |
| State (client) | Zustand | Locked |
| File storage | Cloudflare R2 | Locked |
| Deploy: frontend | Vercel | Locked |
| Deploy: backend | Railway | Locked |

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2026-03-26 | Initial constitution — distilled from CLAUDE.md + BACKEND/FRONTEND_GUIDELINES | CS |
| 2026-03-31 | Fix UI library (MUI v7 → shadcn/ui + Tailwind CSS v4) + Routing (TanStack → React Router DOM v7) | CS |
| 2026-04-07 | Add: `async with db.begin()` banned; mass-assignment whitelist required | CS |
