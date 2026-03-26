---
name: refactor-workflow
description: Chi tiết quy trình refactor các module hiện có - từ RCA đến triển khai. Đảm bảo cải tiến mã nguồn một cách tuần tự và giữ tương thích ngược.
allowed-tools:
  - view_file
  - run_command
  - grep_search
  - list_dir
---

# Refactor Workflow Skill (AG Version)

**Mục đích**: Điều phối quy trình refactor hệ thống các module hiện có, đảm bảo cải thiện chất lượng code mà không làm hỏng tính năng đang chạy.

## Khi nào sử dụng

Sử dụng skill này khi:
- ATu yêu cầu: "Refactor module X", "Xử lý nợ kỹ thuật tại Y", "Cải thiện chất lượng code của Z".
- Module hiện tại gặp vấn đề: hiệu suất kém, không đồng nhất, khó bảo trì.
- Cần thay đổi kiến trúc module để đáp ứng yêu cầu mới.
- Phát hiện các "code smell" (trùng lặp, quá phức tạp, phụ thuộc lẫn nhau).

**KHÔNG sử dụng** cho:
- Sửa các bug nhỏ (sửa trực tiếp).
- Thêm tính năng mới (dùng `/module-workflow`).
- Chỉ đổi tên biến hoặc định dạng code đơn thuần.

---

## Tổng quan quy trình

Skill này dẫn dắt qua các giai đoạn refactor chuẩn:

```
Phase 1: Root Cause Analysis (RCA - Phân tích nguyên nhân gốc)
    ↓
Phase 2: Re-Architecture (Tư duy lại kiến trúc - nếu cần)
    ↓
Phase 3: Refactoring Plan (Lập kế hoạch refactor chi tiết)
    ↓
Phase 4: Backend Refactoring (Triển khai Backend)
    ↓
Phase 5: Frontend Refactoring (Triển khai Frontend)
    ↓
Phase 6: Quality Assurance & Verification (Kiểm tra & Xác nhận)
```

---

## Khởi tạo (Initialization)

### Bước 1: Thu thập ngữ cảnh
Hỏi ATu về:
1. **Tên module** cần refactor.
2. **Vấn đề cụ thể** đang gặp phải? (Hiệu suất? Khó maintain? Code bẩn?)
3. **Mức độ ưu tiên** (P0: Chặn workflow khác, P1: Ảnh hưởng user, P2: Chất lượng code).

### Bước 2: Khởi tạo cấu trúc Track Refactor
Chạy script:
```bash
python .agents/skills/refactor-workflow/scripts/init_refactor_track.py --track-id [ID] --module "[Tên Module]" --priority [P0-P3]
```

Công việc này sẽ tạo:
```
conductor/tracks/[track-id]-refactor-[slug]/
├── README.md
├── RCA.md (Root Cause Analysis)
├── ARCHITECTURE_REFACTOR.md (nếu cần)
├── REFACTORING_PLAN.md
└── QA_REPORT.md
```

---

## Phase 1: Root Cause Analysis (RCA)
**Mục đích**: Hiểu rõ cái gì hỏng và tại sao hỏng trước khi sửa.
**Skill hỗ trợ**: `/refactoring-expert`
**Output**: `conductor/tracks/[track-id]/RCA.md`

## Phase 2: Re-Architecture
**Kiến trúc mới phải giải quyết được các issue đã tìm thấy trong RCA.**
**Output**: `conductor/tracks/[track-id]/ARCHITECTURE_REFACTOR.md`

## Phase 3: Refactoring Plan
**Lập kế hoạch theo từng bước nhỏ (incremental steps).** Mỗi bước phải có phương án Rollback.
**Output**: `conductor/tracks/[track-id]/REFACTORING_PLAN.md`

## Phase 4 & 5: Backend & Frontend Implementation
**Thực hiện chỉnh sửa theo Plan.** Sau mỗi bước nhỏ PHẢI chạy lint/type-check hoặc verify-integrity.

## Phase 6: Quality Assurance & Verification
**Mục đích**: Chạy full test và so sánh kết quả trước/sau khi refactor.
**Output**: `conductor/tracks/[track-id]/QA_REPORT.md`

---

## Nguyên tắc vàng của AG
1. **Không Refactor kiểu "Big-Bang"**: Tuyệt đối không viết lại toàn bộ module trong một lần. Chỉ thực hiện những thay đổi nhỏ, an toàn và có thể kiểm chứng.
2. **Luôn có Backup**: Gắn git tag hoặc backup trước khi bắt đầu.
3. **Kiểm tra sau mỗi bước**: Không đợi đến cuối mới test.
4. **Giữ tương thích ngược**: Tránh làm hỏng các module khác đang gọi module này.
