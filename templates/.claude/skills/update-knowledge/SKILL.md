---
name: update-knowledge
description: Tong ket phien lam viec, luu kien thuc vao Project Memory va chuan bi cho phien tiep theo. Dung khi ket thuc mot task hoac cuoi ngay lam viec.
---

# Update Knowledge Skill

Su dung skill nay de tong ket va luu tru kien thuc sau moi phien lam viec.

## Khi nao dung
- Ket thuc mot task lon
- Cuoi ngay lam viec
- Phat hien kien thuc moi quan trong
- Giai quyet xong mot bug kho

## He thong Memory (Fragmented)

```
Layer 1 — Auto-load (Claude Code tu xu ly):
  .claude/CLAUDE.md              → Repo-wide instructions (KHONG sua o day)
  docs/memory/MEMORY.md          → Quick index

Layer 2 — Lazy-load theo thu muc (Claude Code tu xu ly):
  frontend/CLAUDE.md             → Static frontend patterns (KHONG sua o day)
  backend/CLAUDE.md              → Static backend patterns (KHONG sua o day)

Layer 3 — Fragmented Memory (update-knowledge viet vao day):
  docs/memory/00_active_context.md        → Trang thai hien tai
  docs/memory/01_frontend_guidelines.md   → Frontend rules/bugs
  docs/memory/02_backend_guidelines.md    → Backend rules/bugs
  docs/memory/03_devops_infra.md          → DevOps/Config
  docs/memory/04_tech_decisions_log.md    → Lich su quyet dinh kien truc

Session State:
  docs/memory/session_save.md             → Luu state de resume session sau
```

**Quy tac**: `update-knowledge` chi viet vao **Layer 3** (`docs/memory/`). KHONG chinh sua CLAUDE.md files (Layer 1, 2).

## Quy trinh thuc hien

### 1. Review Session (Danh gia phien lam viec)
- Nhin lai cac tool da goi va task da hoan thanh trong conversation nay.
- Xac dinh "Kien thuc moi" nao quan trong (bug fix, pattern, gotcha).
- Bo qua nhung gi da co trong CLAUDE.md files hoac da co trong `docs/memory/`.

### 2. Importance Scoring (Danh gia muc do quan trong)

Truoc khi ghi vao memory, danh gia moi kien thuc:

| Score | Tieu chi | Hanh dong |
|-------|----------|-----------|
| **P0 — Critical** | Gay production bug, data loss, security issue | ✅ GHI NGAY + danh dau `⚠️` |
| **P1 — Important** | Pattern lap lai ≥2 lan hoac anh huong nhieu module | ✅ GHI vao memory |
| **P2 — Useful** | Trick hay nhung chi ap dung 1 cho cu the | ⏳ GHI neu file chua qua dai |
| **P3 — Trivial** | Kien thuc hien nhien, de tim lai trong code | ❌ KHONG GHI — tranh bloat |

**Rule**: Chi ghi P0 + P1 bat buoc. P2 tuy dung luong. P3 never.

### 3. Update Fragmented Memory (`docs/memory/`)

Phan loai va ghi vao file tuong ung:
- 📍 **Status Project**: Cap nhat `docs/memory/00_active_context.md`
- 🎨 **Frontend rules/bugs**: Ghi vao `docs/memory/01_frontend_guidelines.md`
- 🗄 **Backend rules/bugs**: Ghi vao `docs/memory/02_backend_guidelines.md`
- 🚀 **DevOps/Config**: Ghi vao `docs/memory/03_devops_infra.md`
- 📚 **Logic/Decisions**: Ghi vao `docs/memory/04_tech_decisions_log.md`

Doc noi dung cu truoc, roi dung `edit` de chen thong tin moi. Viet ngan gon suc tich bang tieng Viet.

**Format ghi**:
```
### [P0/P1/P2] Ten kien thuc (YYYY-MM-DD)
- **Van de**: ...
- **Giai phap**: ...
- **Ap dung khi**: ...
```

### 4. Memory Pruning (Dinh ky)

Khi memory file vuot **40KB**:
- Review cac entry P2 cu hon 30 ngay → xoa neu khong con relevant
- Merge cac entry trung lap thanh 1
- Giu nguyen P0 + P1 entries (khong bao gio xoa)

### 5. Update Track Transition Ledger

Neu track co thay doi status trong session nay, ghi vao `CHANGELOG.md` trong folder track:

```markdown
## Changelog
| Date | From | To | Agent | Note |
|------|------|----|-------|------|
| 2026-03-16 | 📅 Planned | 💻 Dev | CS | Bat dau implement backend |
| 2026-03-17 | 💻 Dev | 🧪 QA | CS | Backend + Frontend done, cho ATu test |
```

Dong thoi update status trong `conductor/tracks.md`.

### 6. Session Save (Luu trang thai session)

Ghi file `docs/memory/session_save.md` voi format:

```markdown
# Session Save
> Saved: YYYY-MM-DD HH:MM

## Track dang lam
- Track [ID]: [Ten] — [Status hien tai]

## Da hoan thanh trong session nay
- [Liet ke ngan gon]

## Dang do dang
- [Task/step cu the chua xong]

## Next Steps
- [Buoc tiep theo can lam ngay khi resume]

## Context can nho
- [Bien, state, decision quan trong ma session sau can biet]
```

**Rule**: File nay bi **overwrite** moi lan save. Chi giu state moi nhat.

### 7. Maintain Zero-Loop Skill
- Neu phat hien quy trinh lap hoac loi he thong moi → update `.agent/skills/zero-loop-dev/SKILL.md`

### 8. Final Report

Bao cao cho ATu:
- Da luu [X] entries (P0: N, P1: N)
- Track [ID] status: [old] → [new]
- Session saved ✓
- Goi y: "Lan sau go `/new-conversation` de em load lai context"

## Files lien quan (Layer 3 - chi viet vao day)

| File | Muc dich |
|------|----------|
| `docs/memory/00_active_context.md` | Trang thai hien tai |
| `docs/memory/01_frontend_guidelines.md` | Frontend rules/bugs |
| `docs/memory/02_backend_guidelines.md` | Backend rules/bugs |
| `docs/memory/03_devops_infra.md` | DevOps/Config |
| `docs/memory/04_tech_decisions_log.md` | Lich su quyet dinh kien truc |
| `docs/memory/session_save.md` | Session state de resume |
| `conductor/tracks.md` | Tien do tracks |
| `conductor/tracks/<id>/CHANGELOG.md` | Transition ledger per track |

## Lien ket voi cac skill khac
- `/new-conversation` - Nap lai context dau session
- `/conductor` - Quan ly tracks chi tiet
- `/zero-loop-dev` - Scaffold backend entities
