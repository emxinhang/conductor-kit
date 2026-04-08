---
name: deploy-track
description: Dung skill deploy-track de deploy track len production sau khi QA pass - chay Railway backend deploy, Vercel frontend, alembic migration, smoke test production, roi cap nhat conductor track status = Done.
---

# Deploy Track

Huong dan end-to-end deploy mot track da QA-pass len production (Railway + Vercel), bao gom migration, smoke test, va wrap-up.

## When to Use

Sau khi:
- QA checklist da PASS (`/frontend-qa-gatekeeper` hoac `/qa-verify-expert`)
- ATu da test local va chap thuan
- Khong con pending bugs

## Pre-Deploy Checklist

Truoc khi deploy, xac nhan:
- [ ] `npm run build` pass (frontend)
- [ ] `python .claude/skills/zero-loop-dev/scripts/verify_integrity.py` pass (backend)
- [ ] Tat ca files da saved (khong con unsaved changes trong IDE)
- [ ] Migration files da commit vao git (QUAN TRONG — Railway deploy doc tu git)

## Deploy Process

### Buoc 1: Commit Code

```bash
# Kiem tra status
git status
git diff --stat

# Stage va commit (KHONG auto-commit — ATu tu quyet dinh)
# ATu tu chay: git add [files] && git commit -m "..."
```

> **Luu y**: NEVER auto-commit. Nhac ATu commit truoc khi push.

### Buoc 2: Deploy Backend (Railway)

Railway tu dong deploy khi push len `main`. Neu can manual trigger:

```bash
# Kiem tra Railway CLI da install
railway --version

# Deploy (neu dung Railway CLI)
railway up

# Hoac push len main de trigger auto-deploy
git push origin main
```

**Sau khi deploy backend**, chay migration:

```bash
# Option 1: Railway CLI
railway run alembic upgrade head

# Option 2: Qua Railway Dashboard
# Settings → Deploy → "railway run alembic upgrade head"
```

**Verify backend deploy**:
```bash
curl https://[railway-url]/api/v1/health
# Expected: {"status": "ok"} hoac 200
```

### Buoc 3: Deploy Frontend (Vercel)

Vercel auto-deploy khi push len `main`. Kiem tra:
1. Vao Vercel Dashboard → Project → Deployments
2. Xac nhan build thanh cong (green checkmark)
3. Neu fail: xem build logs

**Verify frontend deploy**:
- Mo `https://[vercel-url]` tren browser
- Kiem tra khong co white screen / 404

### Buoc 4: Production Smoke Test

Test cac features chinh cua track vua deploy:

```
For each acceptance criterion trong IMPLEMENTATION_PLAN.md:
  - Test tren production URL (khong phai localhost)
  - Screenshot neu can bao cao
  - Flag bat ky issue nao
```

**Smoke test minimum**:
- [ ] Login thanh cong
- [ ] Feature chinh cua track hoat dong (happy path)
- [ ] Khong co console errors nghiem trong
- [ ] API calls tra ve 200 (check Network tab)

### Buoc 5: Update Conductor

```bash
# Goi /conductor de cap nhat track status
/conductor
```

Cap nhat `conductor/tracks.md`:
- Status: In Progress → Done
- Them note: ngay deploy, version

### Buoc 6: Save Learnings

```bash
/update-knowledge
```

Luu vao project memory:
- Cac bugs tim thay trong track nay
- Patterns tot can nhan ra
- Cac gotchas de tranh lan sau

## Rollback Plan

Neu production bi loi sau deploy:

### Rollback Frontend (Vercel)
1. Vao Vercel Dashboard → Deployments
2. Tim deployment truoc do
3. Click "Promote to Production"

### Rollback Backend (Railway)
```bash
# Revert migration
railway run alembic downgrade -1

# Revert code: push commit cu len main
git revert HEAD
git push origin main
```

### Rollback Database
```bash
railway run alembic downgrade -1
# Neu can revert nhieu buoc:
railway run alembic downgrade [revision_id]
```

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Railway deploy fail | Migration file chua commit | `git add alembic/versions/*.py && git commit` |
| Vercel build fail | TypeScript error | Chay `npm run build` local truoc |
| 500 error sau deploy | Thieu env var | Kiem tra Railway environment variables |
| Migration fail | DB constraint | Kiem tra data hien co, them nullable=True neu can |

## Wrap-Up Confirmation

Sau khi deploy thanh cong:

```
Track [ID] - [Name]
Status: DEPLOYED to Production
Date: [date]
Railway: OK
Vercel: OK
Migration: OK (neu co)
Smoke Test: PASS
Conductor: Updated
Knowledge: Saved
```

## Exit Routine (Bắt buộc)

Sau khi Smoke Test production pass, chạy **2 lệnh** theo thứ tự:

```bash
# 1. Cập nhật badge track trong tracks.md + CHANGELOG
python conductor/status.py transition <track-id> done <agent> "deployed to production"

# 2. Promote PIPELINE[0] → ACTIVE trong state.md
python conductor/status.py done
```

Thay `<track-id>` bằng ID thực tế và `<agent>` bằng agent đang deploy (CS/AG/CD).