---
name: deploy-track
description: Deploy track lên production sau khi QA pass — chạy backend deploy, frontend deploy, migration, smoke test production, rồi cập nhật conductor track status = Done.
---

# Deploy Track

Hướng dẫn end-to-end deploy một track đã QA-pass lên production, bao gồm migration, smoke test, và wrap-up.

## When to Use

Sau khi:
- QA checklist đã PASS (`/qa-verify-expert`)
- User đã test local và chấp thuận
- Không còn pending bugs

## Pre-Deploy Checklist

Trước khi deploy, xác nhận:
- [ ] `npm run build` pass (frontend)
- [ ] `python .claude/skills/zero-loop-dev/scripts/verify_integrity.py` pass (backend)
- [ ] Tất cả files đã saved (không còn unsaved changes)
- [ ] Migration files đã commit vào git (QUAN TRỌNG — deploy platform đọc từ git)

## Deploy Process

### Bước 1: Commit Code

```bash
# Kiểm tra status
git status
git diff --stat

# Stage và commit (KHÔNG auto-commit — user tự quyết định)
# User tự chạy: git add [files] && git commit -m "..."
```

> **Lưu ý**: NEVER auto-commit. Nhắc user commit trước khi push.

### Bước 2: Deploy Backend

Push lên `main` để trigger auto-deploy (hoặc theo quy trình deploy của dự án):

```bash
git push origin main
```

**Sau khi deploy backend**, chạy migration nếu có:

```bash
# Theo hướng dẫn deploy của dự án
# Ví dụ: railway run alembic upgrade head
```

**Verify backend deploy**:
```bash
curl https://[your-api-url]/api/v1/health
# Expected: {"status": "ok"} hoặc 200
```

### Bước 3: Deploy Frontend

Frontend thường auto-deploy khi push lên `main`. Kiểm tra:
1. Vào Dashboard của platform → Project → Deployments
2. Xác nhận build thành công (green checkmark)
3. Nếu fail: xem build logs

**Verify frontend deploy**:
- Mở URL production trên browser
- Kiểm tra không có white screen / 404

### Bước 4: Production Smoke Test

Test các features chính của track vừa deploy:

```
For each acceptance criterion trong IMPLEMENTATION_PLAN.md:
  - Test trên production URL (không phải localhost)
  - Screenshot nếu cần báo cáo
  - Flag bất kỳ issue nào
```

**Smoke test minimum**:
- [ ] Login thành công
- [ ] Feature chính của track hoạt động (happy path)
- [ ] Không có console errors nghiêm trọng
- [ ] API calls trả về 200 (check Network tab)

### Bước 5: Update Conductor

```bash
# Gọi /conductor để cập nhật track status
/conductor
```

Cập nhật `conductor/tracks.md`:
- Status: In Progress → Done
- Thêm note: ngày deploy, version

### Bước 6: Save Learnings

```bash
/update-knowledge
```

Lưu vào project memory:
- Các bugs tìm thấy trong track này
- Patterns tốt cần nhân ra
- Các gotchas để tránh lần sau

## Rollback Plan

Nếu production bị lỗi sau deploy:

### Rollback Frontend
1. Vào Dashboard của platform → Deployments
2. Tìm deployment trước đó
3. Promote về Production

### Rollback Backend
```bash
# Revert migration
# alembic downgrade -1

# Revert code: push commit cũ lên main
git revert HEAD
git push origin main
```

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Backend deploy fail | Migration file chưa commit | `git add alembic/versions/*.py && git commit` |
| Frontend build fail | TypeScript error | Chạy `npm run build` local trước |
| 500 error sau deploy | Thiếu env var | Kiểm tra environment variables trên platform |
| Migration fail | DB constraint | Kiểm tra data hiện có, thêm nullable=True nếu cần |

## Exit Routine (Bắt buộc)

Sau khi Smoke Test production pass, chạy **2 lệnh** theo thứ tự:

```bash
# 1. Cập nhật badge track trong tracks.md + CHANGELOG
python conductor/status.py transition <track-id> done <agent> "deployed to production"

# 2. Promote PIPELINE[0] → ACTIVE trong state.md
python conductor/status.py done
```

Thay `<track-id>` bằng ID thực tế và `<agent>` bằng agent đang deploy (CS/AG/CD).

## Wrap-Up Confirmation

Sau khi deploy thành công:

```
Track [ID] - [Name]
Status: DEPLOYED to Production
Date: [date]
Backend: OK
Frontend: OK
Migration: OK (nếu có)
Smoke Test: PASS
Conductor: Updated
Knowledge: Saved
```
