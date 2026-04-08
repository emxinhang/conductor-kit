---
name: module-workflow
description: Chi tiết quy trình xây dựng module mới - từ Requirements đến QA. Tự động khởi tạo cấu trúc track, template và validate từng phase.
allowed-tools:
  - view_file
  - write_to_file
  - run_command
  - list_dir
---

# Module Workflow Skill (AG Version)

**Mục đích**: Điều phối quy trình 6 bước hoàn chỉnh để xây dựng module mới trong TMS-2026, đảm bảo tiếp cận hướng kiến trúc (Architecture-First) và chất lượng Zero-Loop.

## Khi nào sử dụng

Sử dụng skill này khi:
- Bắt đầu một module hoặc tính năng mới (ví dụ: Invoice, Booking, Reports).
- User yêu cầu: "Tạo module mới X", "Xây dựng tính năng Y", "Bắt đầu track cho Z".
- Bắt đầu một track công việc bao gồm cả backend và frontend.

**KHÔNG sử dụng** cho:
- Sửa bug nhỏ.
- Thay đổi UI đơn thuần.
- Refactor nhanh.
- Cập nhật tài liệu.

---

## Tổng quan quy trình (6 Phases)

Skill này dẫn dắt qua **6 giai đoạn** được định nghĩa trong [WORKFLOW_STANDARD.md](../../../docs/WORKFLOW_STANDARD.md):

```
Phase 1: Requirements Discovery (Khám phá yêu cầu - có thể bỏ qua)
    ↓
Phase 2: Architecture Design (Thiết kế kiến trúc - BẮT BUỘC)
    ↓
Phase 3: Detailed Planning (Lập kế hoạch chi tiết - Sonnet 4.5/AG)
    ↓
Phase 4: Backend Implementation (Triển khai Backend - Zero-Loop)
    ↓
Phase 5: Frontend Implementation (Triển khai Frontend - Standard V1)
    ↓
Phase 6: Quality Assurance & Review (Kiểm soát chất lượng & Review)
```

---

## Khởi tạo (Initialization)

### Bước 1: Thu thập ngữ cảnh
Hỏi ATu về:
1. **Tên module** (ví dụ: "Quản lý Hóa đơn")
2. **Track ID** (Gợi ý ID tiếp theo, ví dụ: "048")
3. **Mô tả ngắn** (1-2 câu)
4. **Yêu cầu đã sẵn sàng chưa?**
   - Nếu RỒI → Nhảy sang Phase 2.
   - Nếu CHƯA → Bắt đầu từ Phase 1.

### Bước 2: Khởi tạo cấu trúc Track
Chạy script khởi tạo (sử dụng đường dẫn tuyệt đối):
```powershell
python t:\01-code\TMS-2026\.agent\skills\module-workflow\scripts\init_track.py --track-id [ID] --name "[Tên Module]" --description "[Mô tả]"
```

Công việc này sẽ tạo:
```
conductor/tracks/[track-id]-[slug]/
├── README.md
├── PRD.md (nếu cần Phase 1)
├── ARCHITECTURE.md (template)
├── IMPLEMENTATION_PLAN.md (template)
└── .phase (theo dõi giai đoạn hiện tại)
```

### Bước 3: Cập nhật tracks.md
Thêm entry vào `conductor/tracks.md`.

---

## Phase 1: Requirements Discovery
**Mục đích**: Làm rõ yêu cầu sản phẩm (PRD).
**Skill hỗ trợ**: `t:\01-code\TMS-2026\.agent\skills\requirements-analyst\SKILL.md`
**Output**: `conductor/tracks/[track-id]/PRD.md`

## Phase 2: Architecture Design
**Mục đích**: Thiết kế hệ thống trước khi code. KHÔNG BAO GIỜ SKIP.
**Skills hỗ trợ**: `system-architect`, `backend-architect`, `frontend-architect`.
**Output**: `conductor/tracks/[track-id]/ARCHITECTURE.md`

## Phase 3: Detailed Planning
**Mục đích**: AG lập kế hoạch triển khai chi tiết từng file.
**Output**: `conductor/tracks/[track-id]/IMPLEMENTATION_PLAN.md`

### Phase 3.5: Architectural Critique (Red Team Review)
**Mục đích**: Phản biện kiến trúc Plan vừa viết bằng dữ liệu thực từ codebase.
**Skill**: `t:\01-code\TMS-2026\.agent\skills\red-team-reviewer\SKILL.md`
**Quy trình**:
1. ATu quăng Plan cho Codex/Cursor: *"Check codebase xem plan này đụng file nào, có tái sử dụng được gì không"*
2. ATu call `@[/red-team-reviewer]` + paste Codex report vào
3. Claude Red Team → xuất Plan delta
4. ATu approve → Claude apply → **IMPLEMENTATION_PLAN.md v2**
5. Tiếp tục `/review-plan` (technical checklist) trên v2

**Lưu ý**: Phase 3.5 có thể skip nếu Plan nhỏ (<10 tasks). Không skip nếu có DB schema change hoặc feature phức tạp.

## Phase 4: Backend Implementation
**Mục đích**: Triển khai Backend và verify integrity.
**Skill hỗ trợ**: `t:\01-code\TMS-2026\.agent\skills\zero-loop-dev\SKILL.md`
**Lệnh quan trọng**:
```powershell
python .agent/skills/zero-loop-dev/scripts/scaffold_backend.py [entity]
python .agent/skills/zero-loop-dev/scripts/verify_integrity.py
```

## Phase 5: Frontend Implementation
**Mục đích**: Triển khai UI theo chuẩn TMS-2026.
**Skill hỗ trợ**: `t:\01-code\TMS-2026\.agent\skills\frontend-standard-v1\SKILL.md`

## Phase 6: Quality Assurance & Review
**Mục đích**: Review code, refactor code smell và báo cáo QA.
**Skill hỗ trợ**: `t:\01-code\TMS-2026\.agent\skills\refactoring-expert\SKILL.md`
**Output**: `conductor/tracks/[track-id]/QA_REPORT.md`

---

## Lưu ý quan trọng cho AG
- **Lưu file**: Mọi file kế hoạch (PRD, Architecture, Plan) phải nằm trong folder của track.
- **Verification**: Luôn chạy lệnh kiểm tra trước khi báo hoàn thành một phase.
- **Approval**: Xin xác nhận của ATu sau mỗi phase quan trọng.
