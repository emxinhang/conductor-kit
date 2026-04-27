# Skill Update Guide — I-Ching Project

> Dành cho AI agents (Gemini, Codex, Claude instances khác) cần cập nhật skills của dự án.
> **Ngày tạo**: 2026-04-16 | **Tác giả**: CS (Claude Sonnet)

---

## Tổng quan hệ thống Skills

Skills là các file Markdown định nghĩa workflow cho từng loại task. Claude Code tự động load skill khi người dùng gọi `/skill-name`.

```
.claude/skills/
  <skill-name>/
    skill.md       ← nội dung skill (file duy nhất cần quan tâm)
```

**Format bắt buộc của mỗi skill.md:**
```markdown
---
name: skill-name
description: Mô tả ngắn gọn hiển thị trong menu
---

# Skill Title
[nội dung]
```

---

## Danh sách Skills thuộc Conductor Workflow

Đây là 8 skills cốt lõi của Conductor — chúng liên kết với nhau thành một pipeline. Khi sửa một skill, cần đảm bảo không phá vỡ consistency với các skill khác.

| Skill | File | Vai trò trong pipeline |
|-------|------|----------------------|
| `brainstorm-track` | `.claude/skills/brainstorm-track/skill.md` | Phase 1: Discovery → PRD → contract_delta.md |
| `planner-track` | `.claude/skills/planner-track/skill.md` | Phase 2: Implementation Plan + OpenAPI update |
| `review-plan` | `.claude/skills/review-plan/skill.md` | Gate: review plan trước khi code |
| `handoff` | `.claude/skills/handoff/skill.md` | Kickoff execution: contract check + Zero-Loop |
| `done-checklist` | `.claude/skills/done-checklist/skill.md` | Exit gate: contract validate + build + logic |
| `conductor` | `.claude/skills/conductor/skill.md` | Orchestrator: resources + QA gate |
| `new-conversation` | `.claude/skills/new-conversation/skill.md` | Session start: load context + contracts |
| `update-knowledge` | `.claude/skills/update-knowledge/skill.md` | Session end: save learnings + registry sync |

---

## Contract-First Workflow (tích hợp vào skills từ 2026-04-16)

Từ Track 014 trở đi, dự án áp dụng **Design-First API contract**. Mỗi skill đã được cập nhật với các bước contract tương ứng. Khi update skills, phải **bảo toàn** các bước này:

### Checkpoint contract trong mỗi skill

| Skill | Contract touchpoint (KHÔNG được xóa) |
|-------|--------------------------------------|
| `brainstorm-track` | Phase 4: tạo `contract_delta.md` |
| `planner-track` | Phase 1 bước 3: Contract Delta Check + `make sync-types` |
| `review-plan` | Category 6: Contract Consistency |
| `handoff` | Bước 2: `make validate-contracts` |
| `done-checklist` | Bước 0: Contract Gate |
| `conductor` | QA Gate: `make validate-contracts` |
| `new-conversation` | Profile `planning`: load `docs/contracts/_registry.md` |
| `update-knowledge` | Bước 5.5: Contract Registry Sync |

### Files contract (đọc trước khi sửa skills)

```
docs/contracts/
  FRAMEWORK.md              ← Quy trình đầy đủ, đọc trước
  _registry.md              ← Index contracts hiện tại
  api/ha_lac.yaml           ← OpenAPI spec
  engine/ha_lac_computation.md ← Engine contract
```

---

## Quy tắc khi update skill

### Được làm
- Thêm bước mới vào cuối workflow
- Cập nhật lệnh bash (path thay đổi, tool mới)
- Thêm ví dụ, gotcha, best practice
- Cập nhật template format
- Sửa lỗi typo, clarify wording

### KHÔNG được làm
- Xóa bất kỳ "Contract touchpoint" nào trong bảng ở trên
- Thay đổi Enter/Exit Routine của brainstorm/planner mà không update `conductor/workflow.md`
- Thêm dependency tool mới vào `allowed-tools` frontmatter mà không test
- Thay đổi tên skill trong frontmatter `name:` (sẽ break `/skill-name` invocation)
- Merge 2 skills thành 1 mà không có approval từ ATu

---

## Cách update một skill cụ thể

### Bước 1: Đọc file hiện tại
```
Đọc: .claude/skills/<skill-name>/skill.md
```

### Bước 2: Kiểm tra consistency
Nếu skill có trong bảng "Contract touchpoint" ở trên → verify checkpoint vẫn còn nguyên sau khi sửa.

### Bước 3: Sửa nội dung
Chỉ sửa phần cần thiết. Không reformat toàn bộ file.

### Bước 4: Kiểm tra cross-skill consistency
Nếu bạn thêm bước mới vào `brainstorm-track` → kiểm tra `planner-track` có cần nhận input từ bước đó không.

### Bước 5: Update conductor/workflow.md nếu cần
Nếu thay đổi ảnh hưởng đến toàn pipeline (không phải chỉ 1 skill) → update `conductor/workflow.md` để đồng bộ.

---

## Pipeline flow hiện tại (để hiểu dependencies)

```
/brainstorm-track
  └── Output: PRD.md + spec.md + contract_delta.md (track 014+)
       ↓
/planner-track
  └── Input: spec.md + contract_delta.md
  └── Output: IMPLEMENTATION_PLAN.md + tasks.md
              + docs/contracts/api/ha_lac.yaml (updated)
              + frontend/src/types/_generated/ (generated)
       ↓
/review-plan
  └── Input: IMPLEMENTATION_PLAN.md + contract_delta.md
  └── Output: review report, plan updated nếu có issue
       ↓
ATu approve
       ↓
/handoff
  └── Check: make validate-contracts
  └── Execute: Zero-Loop V3 task by task
       ↓
/done-checklist
  └── Gate 0: make validate-contracts
  └── Gate 1-5: backend, frontend, logic, cleanup, codemap
       ↓
/update-knowledge
  └── Bước 5.5: docs/contracts/_registry.md sync
  └── Save session, learnings
```

---

## Thêm skill mới liên quan đến Conductor

Nếu cần tạo skill mới tham gia vào Conductor pipeline:

1. Đọc `.claude/skills/skill-creator/skill.md` để biết format chuẩn
2. Đặt file tại `.claude/skills/<skill-name>/skill.md`
3. Thêm vào bảng trong file này (Danh sách Skills + Contract touchpoint nếu có)
4. Update `conductor/workflow.md` section "Contract-First Workflow"
5. Update `conductor/tracks.md` nếu skill thay đổi state machine

---

## Tài nguyên liên quan

| File | Mục đích |
|------|---------|
| `conductor/workflow.md` | Workflow reference canonical — source of truth |
| `conductor/constitution.md` | Architectural invariants — không vi phạm |
| `conductor/state.md` | ACTIVE track, PIPELINE queue |
| `docs/contracts/FRAMEWORK.md` | Contract-First workflow chi tiết |
| `docs/contracts/_registry.md` | Danh sách contracts hiện tại |
| `.claude/skills/README.md` | Overview tất cả skills |
| `.claude/skills/SKILLS_CATALOG_VI.md` | Catalog tiếng Việt |
