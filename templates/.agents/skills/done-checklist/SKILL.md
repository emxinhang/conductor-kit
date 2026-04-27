---
name: done-checklist
description: Exit checklist bắt buộc chạy trước khi mark track là ✅ Completed. Ngăn chặn finetune/debug tracks bằng cách catch vấn đề trước khi bàn giao. Dùng ngay trước khi nói "Done" với bất kỳ track nào.
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Done Checklist — Exit Gate trước khi mark ✅ Completed

**Tại sao:** 45/133 tracks (34%) là finetune/debug/fix sau khi mark done. Checklist này là gate ngăn track chuyển sang Completed khi vẫn còn vấn đề có thể catch được ngay lúc này.

**Khi nào dùng:** Ngay trước khi báo "Done" hoặc chuyển track sang ✅ Completed.

---

## Bước 0: Contract Gate (track 014+ — nếu có API/DB changes)

Bỏ qua bước này nếu track không có API mới hoặc không thay đổi API shape.

```bash
# 0a. Validate live API vs committed spec
make validate-contracts
# Kết quả: "OK" hoặc danh sách drift

# 0b. Check TypeScript generated types đã được sync
ls frontend/src/types/_generated/
```

**Tiêu chuẩn xanh:**
- [ ] `make validate-contracts` → **OK** (không có drift giữa code và spec)
- [ ] `frontend/src/types/_generated/` tồn tại và đã được commit nếu có API changes
- [ ] `docs/contracts/_registry.md` đã cập nhật version + date cho contract vừa thay đổi
- [ ] Breaking changes (nếu có) đã được ghi vào `docs/contracts/_registry.md` Breaking Change Log

---

## Bước 1: Backend Gate (nếu có thay đổi backend)

```bash
# 1a. Verify integrity — models, routers, schemas đều đăng ký đúng
cd backend; python .agents/skills/zero-loop-dev/scripts/verify_integrity.py

# 1b. Không còn debug prints
grep -r "print(" app/ --include="*.py" | grep -v "#" | grep -v "test_"

# 1c. Migration có downgrade()
# → Xem alembic-workflow skill để check
```

**Tiêu chuẩn xanh:**
- [ ] `verify_integrity.py` pass, không có lỗi import
- [ ] Không có `print(` debug còn sót trong `app/` (ngoài test files)
- [ ] Migration mới nhất có `downgrade()` không phải `pass`
- [ ] API endpoint mới có error handling (try/except hoặc HTTPException)
- [ ] Schema mới có đủ `CreateSchema`, `UpdateSchema`, `ResponseSchema`

---

## Bước 2: Frontend Gate (nếu có thay đổi frontend)

```bash
# 2a. TypeScript check — BLOCKING
cd frontend; npx tsc --noEmit 2>&1 | tail -30

# 2b. Không có any types mới được thêm vào
cd frontend; git diff --name-only | xargs grep -l ": any\|as any" 2>/dev/null

# 2c. Build pass
cd frontend; npm run build 2>&1 | tail -15
```

**Tiêu chuẩn xanh:**
- [ ] `tsc --noEmit` → **0 errors** (blocking — không pass = không done)
- [ ] Không có `": any"` hoặc `"as any"` mới trong files đã sửa
- [ ] `npm run build` pass, 0 errors
- [ ] Route mới đã đăng ký trong `App.tsx`
- [ ] Navigation sidebar hiển thị đúng (nếu thêm module mới)

---

## Bước 3: Logic & Edge Cases

Tự trả lời 3 câu hỏi này trước khi mark done:

**Q1: Happy path có chạy không?**
→ Đã test thủ công luồng chính (create → read → update → delete nếu có)?

**Q2: Error path có xử lý không?**
→ Nếu API trả 4xx/5xx, UI có hiện toast error thay vì crash?

**Q3: Empty state có xử lý không?**
→ List rỗng, field null, user không có permission — UI có hiển thị đúng?

- [ ] Happy path tested
- [ ] Error path có toast/fallback
- [ ] Empty state không crash

---

## Bước 4: Không để lại rác

```bash
# Debug artifacts còn sót
grep -r "TODO\|FIXME\|HACK\|console\.log\|debugger" frontend/src --include="*.ts" --include="*.tsx" | grep -v ".test." | grep -v "//.*TODO"
```

- [ ] Không có `console.log` debug trong frontend files đã sửa
- [ ] Không có `TODO` / `FIXME` chưa resolve trong code mới
- [ ] Không có file test tạm (`test_*.py`, `*.tmp`) bị commit

---

## Bước 5: Cập nhật Codebase Map (Track 142)

**Tại sao:** Đảm bảo `docs/codebase-map.md` luôn phản ánh đúng cấu trúc hiện tại của dự án cho các phiên làm việc sau.

```bash
# Cập nhật bản đồ cấu trúc mã nguồn
python tools/gen_codemap.py
```

**Tiêu chuẩn xanh:**
- [ ] `tools/gen_codemap.py` chạy không lỗi.
- [ ] File `docs/codebase-map.md` đã được cập nhật.

---

## Report Format khi Done

Sau khi pass tất cả gates, báo cáo:

```
✅ Done Checklist PASSED — Track [ID]

Contract (nếu có API changes):
  - validate-contracts: ✅ OK / ❌ drift detected
  - types synced: ✅ / ❌
  - registry updated: ✅ / N/A

Backend:
  - verify_integrity: ✅ pass
  - migrations: ✅ downgrade() có
  - no debug prints: ✅

Frontend:
  - tsc --noEmit: ✅ 0 errors
  - no new `any`: ✅
  - build: ✅ pass

Logic:
  - Happy path: ✅ tested [mô tả ngắn]
  - Error path: ✅ toast error hoạt động
  - Empty state: ✅ handled

→ ATu check UI tại: [route]
```

---

## Nếu một gate FAIL

**Không mark done.** Fix trước, chạy lại gate đó, báo cáo kết quả mới.

Nếu fail quá phức tạp để fix trong scope hiện tại → tạo sub-track mới (vd: `XXX-debug`) và ghi rõ trong CHANGELOG của track hiện tại trước khi close.
