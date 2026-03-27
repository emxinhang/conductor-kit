---
name: atu-conductor
description: Cách vận hành quy trình Conductor (Vietnamese Version) để quản lý tính năng và lỗi cho dự án.
---

# Skill: Conductor (Quản lý Track & Điều phối)

Dùng skill này để điều phối công việc giữa 3 agents (CS, AG, CD) đảm bảo nguyên tắc **Cuốn chiếu: 1 implementation tại 1 thời điểm**.

## 1. Vai trò của Agents

| Agent | Tool | Role |
|---|---|---|
| **CS** | Claude Sonnet | Orchestrator — Brainstorm, PRD, Plan, Review |
| **AG** | Gemini | Implementer — Code Backend/Frontend theo Plan |
| **CD** | Codex | Implementer — Code, Debug (Dự phòng cho AG) |

## 2. Shared State & Dashboard

Mọi agent bắt đầu session bằng cách kiểm tra tình trạng dự án:
- **Đọc `conductor/state.md`**: Nguồn truth duy nhất về ACTIVE/PIPELINE/DONE.
- **Dùng Dashboard**: Chạy lệnh `python conductor/status.py`.

## 3. Quy trình làm việc (Workflow)

### CS (Planning Role)
1. Read `state.md` + `session_save_cs.md`.
2. Brainstorm → PRD → Plan (trong `conductor/tracks/[id]/`).
3. Chốt Plan: Cập nhật track vào **PIPELINE** trong `state.md`.
4. Run `/update-knowledge` để lưu session.

### AG / CD (Implementation Role)
1. Read `state.md` → Thấy track trong **ACTIVE**.
2. Read `conductor/tracks/[id]/SESSION.md` để tiếp tục context.
3. Implement code & Verify (Zero-Loop).
4. Khi Done: Chạy `python conductor/status.py done`.
5. Khi Pause: Run `/update-knowledge` để lưu session.

## 4. Các lệnh quan trọng

```bash
python conductor/status.py              # Xem dashboard
python conductor/status.py done         # Xong ACTIVE, đẩy PIPELINE[0] lên
python conductor/status.py note "..."   # Ghi chú cho track đang làm
python conductor/status.py add "name"   # Thêm vào BACKLOG

# Transition tự động sync state.md + CHANGELOG.md:
python conductor/status.py transition <id> planned <agent> "<note>"  # → UPCOMING→PIPELINE
python conductor/status.py transition <id> dev <agent> "<note>"      # → PIPELINE→ACTIVE
python conductor/status.py transition <id> qa <agent> "<note>"       # → warn nếu thiếu qa/
python conductor/status.py transition <id> done <agent> "<note>"     # → ACTIVE→DONE

# Shortcut cho done:
python conductor/status.py close <id> [agent] [note]               # = transition <id> done
```

## 5. QA Gate (bắt buộc trước khi transition → qa)

Trước khi chạy `python conductor/status.py transition <id> qa`:
- [ ] **Frontend build**: `npm run build` chạy không lỗi
- [ ] **Backend runtime**: script QA chạy được trong venv
- [ ] **Artifact saved**: script + log output đã lưu vào `conductor/tracks/<id>/qa/`
- [ ] **Gitignore safe**: thư mục `qa/` không bị `.gitignore` chặn

`status.py` sẽ **tự động warn** nếu chưa có thư mục `qa/`.

## 6. Cấu trúc Folder Track
- `spec.md`: Yêu cầu chi tiết.
- `plan.md`: Kế hoạch thực hiện.
- `SESSION.md`: Trạng thái dở dang (chỉ dành cho Implementation).
- `CHANGELOG.md`: Nhật ký thay đổi trạng thái.

