---
name: deploy-track
description: Deploy track lên production sau khi QA pass — chạy backend deploy, frontend deploy, migration, smoke test production, rồi cập nhật conductor track status = Done.
---

# Deploy Track

Hướng dẫn end-to-end deploy một track đã QA-pass lên production, bao gồm migration, smoke test, và wrap-up.

## When to Use

Sau khi:
- QA checklist đã PASS
- User đã test local và chấp thuận
- Không còn pending bugs

## Pre-Deploy Checklist

- [ ] `npm run build` pass (frontend)
- [ ] `verify_integrity.py` pass (backend)
- [ ] Migration files đã commit vào git
- [ ] Tất cả files đã saved

## Deploy Process

### Bước 1: Commit Code
> NEVER auto-commit. Nhắc user commit trước khi push.

```bash
git status && git diff --stat
```

### Bước 2: Deploy Backend
Push lên `main` để trigger auto-deploy, sau đó chạy migration theo hướng dẫn của dự án.

**Verify**: `curl https://[api-url]/api/v1/health` → 200 OK

### Bước 3: Deploy Frontend
Auto-deploy khi push lên `main`. Kiểm tra build thành công trên platform Dashboard.

**Verify**: Mở production URL, không có white screen.

### Bước 4: Production Smoke Test

- [ ] Login thành công
- [ ] Feature chính hoạt động (happy path)
- [ ] Không có console errors nghiêm trọng
- [ ] API calls trả về 200

### Bước 5: Update Conductor & Save Learnings

```bash
/conductor    # cập nhật track status
/update-knowledge    # lưu learnings
```

## Exit Routine (Bắt buộc)

```bash
# 1. Transition track → done
python conductor/status.py transition <track-id> done AG "deployed to production"

# 2. Promote PIPELINE → ACTIVE
python conductor/status.py done
```
