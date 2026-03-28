---
name: zero-loop-dev
description: Enforce "Zero-Loop" development workflow V3 — Execution Engine cho Giai đoạn 2. Agent code đến đâu tự verify xanh đến đó, cấm báo hoàn thành mà không có bằng chứng. Use when creating new backend entities or before saying "Backend Done".
---

# Zero-Loop Development Skill V3 (The Execution Engine)

Quy trình **Zero-Loop V3** áp dụng cho Giai đoạn 2 (sau khi đã có `IMPLEMENTATION_PLAN.md` final). Mục tiêu tối thượng: Code đến đâu, tự Verify (chạy thử) xanh đến đó. **Tuyệt đối không bàn giao code mù cho người dùng test thử.**

## Bước 1: Khởi động (Handoff & Recon)

Khi nhận lệnh `/handoff` hoặc bắt đầu task mới:
- Đọc `IMPLEMENTATION_PLAN.md` mới nhất trong track hiện tại
- Chạy `git status` và `git diff` để xem đã generate file nào
- Chạy `npm run build` (tsc) để check boilerplate có lỗi type/syntax không — xử lý rác trước khi code tiếp

## Bước 2: Thực thi & Code Logic

- Chọn task tiếp theo chưa `[x]` trong plan, làm từng task nhỏ
- **Backend API**: Chạy `python .agent/skills/zero-loop-dev/scripts/verify_integrity.py` sau mỗi entity mới để check import & schemas
- **Frontend**: Không có lỗi TypeScript strict

## Bước 3: Mệnh Lệnh Tối Thượng — Bằng Chứng Hoàn Thành

**CẤM CHUYỂN TASK NẾU CHƯA CÓ BẰNG CHỨNG:**

### Backend
- Tạo script test tạm `scripts/test_{feature}_handoff.py` hoặc dùng `curl`
- Chạy script, đọc terminal output
- **Tiêu chuẩn Xanh**: HTTP 200 OK + JSON data chuẩn → pass
- **Tiêu chuẩn Đỏ**: HTTP 4xx/5xx, exception, wrong data → fix ngay

### Frontend
- Chạy `npm run build` tại `/frontend`
- **Tiêu chuẩn Xanh**: Build pass, zero TypeScript errors, zero unused vars

## Bước 4: Xử lý Lỗi RCA (Cuốn Chiếu)

Nếu Bước 3 Đỏ:
1. Dừng lại, không chuyển task
2. Truy vết root cause
3. Fix minimal change
4. Lặp lại Bước 3 tới khi Xanh

## Bước 5: Báo cáo (The Gate)

Khi hoàn tất cụm task, báo cáo với **bằng chứng thực tế**:

```
✅ Task [X] complete
Backend: HTTP 200 — [paste terminal output snippet]
Frontend: Build pass — 0 errors
→ Đã [x] trong IMPLEMENTATION_PLAN.md
→ User check UI tại: [route/component]
```

---

## Rules cốt lõi

1. **No Manual File Creation** — dùng scaffold cho entity mới
2. **Verify First** — không nói "Backend Done" chưa chạy verify script
3. **Schema Integrity** — thêm field vào Model → update đồng thời `CreateSchema`, `UpdateSchema`, `ResponseSchema`
4. **API Interface Sync** — update Backend Schema → update TypeScript interfaces trong `frontend/src/api/*.ts` trước khi dùng trong component
5. **Evidence Required** — mọi "hoàn thành" phải kèm terminal output hoặc build log

## Exit Routine — Sau khi verify_integrity pass

```bash
python conductor/status.py transition <track-id> qa CD "backend done, ready for QA"
```
