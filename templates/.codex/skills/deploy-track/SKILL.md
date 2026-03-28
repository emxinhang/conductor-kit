---
name: deploy-track
description: Deploy track lên production sau khi QA pass — chạy backend deploy, frontend deploy, migration, smoke test production, rồi cập nhật conductor track status = Done.
---

# Deploy Track

Hướng dẫn end-to-end deploy một track đã QA-pass lên production.

## Pre-Deploy Checklist

- [ ] `npm run build` pass (frontend)
- [ ] `verify_integrity.py` pass (backend)
- [ ] Migration files đã commit vào git
- [ ] Tất cả files đã saved

## Deploy Process

### Bước 1: Commit Code
> NEVER auto-commit. User tự commit và push.

### Bước 2: Deploy Backend + Migration
Push lên `main` để trigger auto-deploy. Sau đó chạy migration theo hướng dẫn của dự án.

### Bước 3: Deploy Frontend
Auto-deploy khi push lên `main`. Kiểm tra build thành công.

### Bước 4: Smoke Test Production

- [ ] Login thành công
- [ ] Feature chính hoạt động
- [ ] Không có console errors
- [ ] API calls trả về 200

## Exit Routine (Bắt buộc)

```bash
python conductor/status.py transition <track-id> done CD "deployed to production"
python conductor/status.py done
```
