# DevOps & Infrastructure Logging

## 🚂 Environment & Workflow (Local/Windows)
- **Venv setup**: Lỗi báo "no module named ..."? Dùng script vòng lặp `setup_and_migrate.ps1` để tự động recreate venv, cài pip reqs, run alembic migrations và kích hoạt lại script `activate.ps1`.
- **Scripts Backend (Isolated)**: Cần chạy lệnh AI/nháp Python trong `scripts/backend/`? Bắt buộc kích hoạt `.venv/Scripts/Activate.ps1` trước. Phải export biến môi trường (ví dụ bằng `$env:ENV_FILE="backend/.env.local"`) để Pydantic config root nạp đúng `DATABASE_URL` và `S3_*`, nếu không crash fail validation startup. Nếu báo lỗi thiếu `Model` trong Registry, import tường minh Model vào đầu hook/script đó.
- **Port 8000 Zombie Stalling**: Uvicorn báo chạy nhưng call bị treo Loading miết? Nguyên nhân do tiến trình Node/Python cũ 8000 chưa bị tắt đúng cách. Tìm process bằng lện PowerShell `Get-NetTCPConnection -LocalPort 8000`, lấy PID và dùng `Stop-Process -Id <PID> -Force`.
- **Trapping Windows Encoding**: Lệnh chuyển hướng PowerShell `>` trên file Jinja2 (HTML) sẽ đổi encode sang UTF-16, gây Backend jinja compiler crash. Luôn check và lưu document chuẩn UTF-8 (without BOM) trên Editor.
- **Git Dubious Ownership**: Windows -> Ổ đĩa rời hoặc Docker volume bị lỗi Trust Git? Chạy định kỳ `git config --global --add safe.directory <thư mục>` để cấp quyền truy xuất commit origin.

## 🚀 Deployment (Railway/Vercel)
- **Database Migrations (Alembic)**: 
  - KHÔNG xóa file config migration manually trừ khi phải chạy script thao tác thẳng vào bảng DB `alembic_version` sửa update revision tương ứng. Alembic sẽ ném lỗi `Can't locate revision` nếu thiếu file link đó.
  - Khi code run lệnh migrate tự động nhưng DB báo lỗi `UndefinedColumnError`, thường do file revision `*.py` mới chưa được add vào git tracking nhánh đó. Cần check `git status`.
- **Mixed Content / HTTPS Loop**: Force schema HTTPS sau SSL Proxy. Uvicorn backend trên Cloud phải gắn `proxy_headers=True` và middleware `ProxyHeadersMiddleware` để không chặn IP client. Loại bỏ các slashes phụ gây loop route.
- **Vercel Build Optimization (Monorepo)**: Dùng custom bash build command `git diff --quiet HEAD^ HEAD .` ở `Settings > Git > Ignored Build Step` của Dashboard Vercel project để Frontend không auto build vô tội vạ rác Log / Credits thời gian nếu Back/Doc/Ops workflow có commit mớ.
- **Railway Hook**: Lỗi dịch vụ backend trên Railway kẹt ở Building nhưng không triển khai App mới? Check Log và Setup thủ công bằng lệnh CLI local `railway up --detach` nếu Server Webhook Github -> Railway timeout chập chờn hoặc kẹt do cache container build bị đầy.

- **[P1][2026-03-18] Codex Hook Fix — Windows subprocess encoding**:
  - **Van de**: `codex_review_trigger.py` fail 3 loi: (1) `codex` not found qua subprocess (npm global khong trong PATH Python venv), (2) Unicode emoji crash cp1252, (3) Prompt truyen sai format
  - **Fix**: `shutil.which("codex")`, `sys.stdout.reconfigure(encoding="utf-8")`, prompt qua stdin + `encoding="utf-8"` cho subprocess
  - **Correct Codex CLI syntax**: `codex exec - --full-auto -o <output_file> -C <workdir>` (KHONG dung `--ask-for-approval` hay `--output-last-message` khong co arg)
  - **File**: `.claude/hooks/codex_review_trigger.py`

- **[2026-03-18] Markdown Encoding Guard (Conductor/Memory files)**:
  - **Van de**: File `.md` trong `conductor/` bi vo dau/loi ky tu khi doc bang Windows PowerShell mac dinh, va co the bi chen null-byte neu append bang luong UTF-16 vao file UTF-8.
  - **Root cause**:
    - `Get-Content` khong chi dinh encoding tren Windows PowerShell de doc UTF-8 no-BOM co the hien thi mojibake.
    - `>` hoac `Set-Content` khong chi dinh encoding co the tao/chen UTF-16LE, gay mixed-encoding trong cung file.
  - **Giai phap**:
    - Luon doc file text quan trong bang `Get-Content -Encoding UTF8`.
    - Neu phai ghi bang shell, dung `Set-Content -Encoding UTF8` hoac uu tien `apply_patch` de giu encoding on dinh.
    - Khi nghi ngo file hong, check null-byte: `[IO.File]::ReadAllBytes(path)` va dem byte `0`; neu >0 thi rewrite lai toan file ve UTF-8.
  - **Ap dung khi**: Cap nhat `CHANGELOG.md`, `tracks.md`, `docs/memory/*.md` tren Windows.

### [P1] RBAC rollout mới phải verify migration + capability refresh (2026-03-25)
- **Vấn đề**: Sau khi sửa code quyền đúng nhưng môi trường test vẫn báo "không thấy quyền mới" hoặc behavior lệch role, nguyên nhân thường không phải setup frontend mà do DB chưa chạy hết migration RBAC/capability hoặc session cũ chưa refresh capability.
- **Giải pháp**:
  - Chạy `alembic upgrade head` trên backend env đang test.
  - Sau rollout capability mới, logout/login lại để auth store nạp capability mới.
  - Khi QA bug quyền, kiểm tra migration state trước khi kết luận code chưa đúng.
- **Áp dụng khi**: QA hoặc deploy các track liên quan RBAC/capabilities.
