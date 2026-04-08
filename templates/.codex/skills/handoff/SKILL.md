---
name: handoff
description: Chuyển giao từ Giai đoạn 1 (Plan) sang Giai đoạn 2 (Execution) — AG tiếp quản từ Claude/Codex, đọc plan, kiểm tra codebase state, rồi thực thi theo Zero-Loop V3. Gọi khi Plan đã finalize và sẵn sàng code.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Handoff Skill (Giai đoạn 2 Kickoff)

Skill này kích hoạt khi ATu gọi `/handoff` — báo hiệu **Plan đã chốt, trao quyền cho AG (Gemini) thực thi**. AG (hoặc Claude khi cần) BẮT BUỘC thực hiện 4 bước theo đúng thứ tự.

## Vị trí trong workflow

```
/planner-track → /red-team-reviewer → /review-plan
                         ↓
              ATu approve Plan final
                         ↓
              [/handoff] ← bạn đang ở đây
                         ↓
         Zero-Loop V3 Execution (code + verify)
                         ↓
              ATu: Manual Test → /bug-report nếu có
```

## Bước 0: Load Skills Bổ Trợ (Mandatory)

BẮT BUỘC nạp skills tùy theo phạm vi task trước khi bắt đầu:
- **Backend**: Load `zero-loop-dev` + `qa-verify-expert`
- **Frontend**: Load `frontend-standard-v1` + `frontend-qa-gatekeeper`
- **Full-stack**: Load tất cả 4 skills trên

---

## Bước 1: Context Absorption (Thẩm thấu Kiến trúc)

- Đọc `IMPLEMENTATION_PLAN.md` mới nhất trong track folder — **bắt buộc đọc toàn bộ**, không skim
- Đọc `CHANGELOG.md` của track nếu có để xem lịch sử transitions
- Xác định: Tổng số tasks, tasks đã `[x]`, task tiếp theo cần làm

Báo ATu:
```
Track [X]: [tên track]
Plan: [N] tasks total, [M] done, starting from Task [K]
```

## Bước 2: State Reconnaissance (Khảo sát Codebase)

Chạy các lệnh sau để check tình trạng code hiện tại:

```bash
git status
git diff --stat
```

Nếu Codex/Cursor đã gen boilerplate:
- Chạy `npm run build` tại `/frontend` → nếu có TypeScript errors → fix trước
- Chạy `python .agent/skills/zero-loop-dev/scripts/verify_integrity.py` → nếu integrity fail → fix trước

**Mục tiêu**: Bắt đầu từ codebase sạch, không có inherited bugs.

## Bước 3: Execution — Zero-Loop V3

Thực thi từng task theo `zero-loop-dev` skill:

- Chọn task tiếp theo chưa `[x]`
- Code task đó
- **Verify ngay** (không đợi cuối):
  - Backend: test script hoặc curl → HTTP 200 + JSON đúng
  - Frontend: `npm run build` → 0 errors
- Đánh `[x]` vào plan → chuyển task tiếp theo

Lặp cho đến khi hết tasks hoặc ATu dừng.

## Bước 4: Completion Gate

Khi hoàn tất tất cả tasks (hoặc một phase):

```
✅ Handoff Phase [Backend/Frontend] Complete

Tasks done: [N]/[N]
Evidence:
  - Backend: [endpoint] → 200 OK [snippet]
  - Frontend: Build pass, 0 errors

→ ATu: Sẵn sàng để manual test tại [URL/route]
→ Nếu có bug: gọi /bug-report để Claude RCA
```

Cập nhật `IMPLEMENTATION_PLAN.md` + `CHANGELOG.md` với transition mới.

---

## Task Bundle Format (Context Isolation)

Để tránh context drift, mỗi task được execute với bundle context tối thiểu:

```markdown
## Task Bundle — Task [N]: [Tên task]

### Mô tả
[1-2 câu mô tả task này làm gì]

### Files cần đọc
- [path/to/relevant/file.py]
- [path/to/relevant/component.tsx]

### Constraints
- [Constraint từ backend/frontend guidelines liên quan]
- [TMS-2026 gotcha nếu có]

### Acceptance Criteria
- [ ] [Tiêu chí cụ thể, có thể test được]
- [ ] [Build/test pass]

### DO NOT TOUCH
- [Files ngoài scope của task này]
```

---

## Quy tắc vàng

- **Không bao giờ** báo "xong" mà không có terminal evidence
- **Không** làm nhiều tasks cùng lúc — một task, verify, rồi mới next
- **Nếu gặp lỗi** → dừng, RCA, fix, re-verify (không skip)
- **Không** tự ý mở rộng scope ngoài task bundle hiện tại
