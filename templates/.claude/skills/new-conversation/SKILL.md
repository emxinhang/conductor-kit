---
name: new-conversation
description: Khoi dong phien lam viec moi, nap context tu Project Memory va kiem tra tien do du an. Dung ngay khi bat dau conversation moi.
---

# New Conversation Skill

Su dung skill nay de khoi dong phien lam viec moi mot cach hieu qua.

## Khi nao dung
- Bat dau conversation moi
- Muon nap lai context du an
- Can kiem tra trang thai hien tai cua du an

## He thong Memory (Fragmented)

```
Auto-loaded boi Claude Code (khong can doc thu cong):
  .claude/CLAUDE.md          → Core rules (da load san)
  frontend/CLAUDE.md         → Frontend patterns (lazy-load khi lam viec o frontend/)
  backend/CLAUDE.md          → Backend patterns (lazy-load khi lam viec o backend/)
  docs/memory/MEMORY.md      → Quick index

Fragmented Memory (doc theo Context Profile):
  docs/memory/00_active_context.md        → Trang thai hien tai, Track dang lam (LUON DOC)
  docs/memory/01_frontend_guidelines.md   → Frontend rules/bugs
  docs/memory/02_backend_guidelines.md    → Backend rules/bugs
  docs/memory/03_devops_infra.md          → DevOps/Config
  docs/memory/04_tech_decisions_log.md    → Lich su quyet dinh kien truc

Session State (per-agent — khong dung chung):
  docs/memory/session_save_cs.md          → CS planning/orchestration context
  conductor/tracks/[id]/SESSION.md        → AG/CD implementation context (agent-agnostic)

Conductor State (shared — moi agent doc truoc):
  conductor/state.md                      → ACTIVE track, PIPELINE queue, DONE recent
  [DEPRECATED] docs/memory/session_save.md → Khong dung nua
```

## Quy trinh thuc hien

### 1. Detect Context Profile

Xac dinh **profile** dua tren yeu cau cua ATu hoac track dang active:

| Profile | Khi nao | Memory can load |
|---------|---------|-----------------|
| `planning` | Track moi, brainstorm, PRD | `00_active_context` + `04_tech_decisions_log` |
| `backend` | Implement/debug backend | `00_active_context` + `02_backend_guidelines` |
| `frontend` | Implement/debug frontend | `00_active_context` + `01_frontend_guidelines` |
| `fullstack` | Track co ca BE+FE | `00_active_context` + `01` + `02` |
| `debugging` | Fix bug, RCA | `00_active_context` + guidelines lien quan |
| `devops` | Deploy, migration, config | `00_active_context` + `03_devops_infra` |

**Mac dinh**: Neu chua ro scope → dung `planning` (nhe nhat). Hoi ATu neu can.

### 2. Load Knowledge Base (theo Profile)

- **Luon doc**: `docs/memory/00_active_context.md` (trang thai hien tai)
- **Theo profile**: Chi doc memory file tuong ung voi profile o bang tren
- **KHONG load tat ca** — tiet kiem token, chi load dung thu can

### 3. Auto-Search Memory (thay vi doc toan bo)

Neu ATu de cap keyword cu the (ten module, ten bug, pattern):
- Dung `Grep` search trong `docs/memory/` voi keyword do
- Chi doc phan relevant thay vi load ca file 49KB
- Vi du: ATu noi "fix timezone bug" → grep `timezone` trong `02_backend_guidelines.md` → doc dung section do

### 4. Load Conductor State + Session

**Buoc 4a — Shared state (moi agent doc truoc):**
- Doc `conductor/state.md` → biet ACTIVE track, PIPELINE queue
- Hoac chay: `python conductor/status.py` (nhanh hon)

**Buoc 4b — Session save theo agent:**
- **CS**: Doc `docs/memory/session_save_cs.md`
- **AG hoac CD**: Doc `conductor/tracks/[active-track]/SESSION.md`
- Neu ton tai → bao ATu: *"Em load duoc session tu lan truoc: [tom tat]. Tiep tuc khong?"*
- Neu khong ton tai → bo qua, tiep tuc binh thuong

### 5. Load AG Style (Nap quy chuan giao tiep)
- Doc `.agent/workflows/atu-style.md`
- Tuan thu cac quy tac ve Ngon ngu (Thinking & Planning bang Tieng Viet)

### 6. Check Conductor (Kiem tra tien do)
- `conductor/state.md` da co ACTIVE + PIPELINE — dung luon
- Doc `conductor/tracks.md` neu can full list
- Kiem tra **CHANGELOG.md** trong track folder neu track dang do

### 7. Status Report & Ready

Bao cao cho ATu:
- **Profile**: `[profile name]`
- **Context loaded**: [Tom tat muc tieu hien tai]
- **Trang thai**: Dang lam [Task X] / Chuan bi lam [Task Y]
- **Session save**: [Neu co — tom tat session truoc]
- Nhac 1-2 luu y quan trong tu Memory neu lien quan den task sap lam

## Files can doc

| File | Auto-load? | Muc dich |
|------|-----------|----------|
| `.claude/CLAUDE.md` | ✅ Auto | Core rules |
| `frontend/CLAUDE.md` | ✅ Lazy | Frontend static patterns |
| `backend/CLAUDE.md` | ✅ Lazy | Backend static patterns |
| `docs/memory/00_active_context.md` | ❌ Luon doc | Trang thai hien tai |
| `docs/memory/01_frontend_guidelines.md` | ❌ Theo profile | Frontend rules/bugs |
| `docs/memory/02_backend_guidelines.md` | ❌ Theo profile | Backend rules/bugs |
| `docs/memory/03_devops_infra.md` | ❌ Theo profile | DevOps/Config |
| `docs/memory/04_tech_decisions_log.md` | ❌ Theo profile | Lich su quyet dinh |
| `conductor/state.md` | ❌ Luon doc | ACTIVE track, PIPELINE queue |
| `docs/memory/session_save_cs.md` | ❌ CS only | CS planning session |
| `conductor/tracks/[id]/SESSION.md` | ❌ AG/CD | Track implementation session |
| `.agent/workflows/atu-style.md` | ❌ Manual | Quy chuan giao tiep |
| `conductor/tracks.md` | ❌ Khi can | Full track list |

## Vi du output

```
Em da nap context du an TMS-2026:

**Profile**: backend
**Trang thai**: Dang lam Track 102 - Booking Core Conversion
**Session save**: Co — session truoc da xong backend models + schemas, dang do API router

**Luu y quan trong**:
- selectinload REQUIRED cho nested relations
- response_model=Schema REQUIRED tren router

Anh muon tiep tuc tu session truoc khong?
```

## Lien ket voi cac skill khac
- `/conductor` - Quan ly tracks chi tiet
- `/update-knowledge` - Luu kien thuc cuoi session
- `/zero-loop-dev` - Scaffold backend entities
