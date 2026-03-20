# DevOps / Infra / Config

> Python env, Gemini API, venv setup

## Python Environment
- **venv**: `.venv/` (Python 3.12)
- **Run**: `.venv/Scripts/python`
- **Packages**: google-genai, python-docx, pdfplumber, PyMuPDF, Pillow
- **Install**: `.venv/Scripts/pip install -r requirements.txt`
- **Quy tắc bắt buộc**: LUÔN LUÔN chạy tất cả các script python trong môi trường ảo `.venv` (VD: `.venv\Scripts\python script.py`) để đảm bảo không xung đột thư viện và đúng phiên bản `google-genai` mới nhất.

## Gemini API Quota
- **Free tier**: RPM 1k, TPM 1M, RPD 10k — đủ batch 2300 trang (~30-40 phút)
- **Paid tier** (ATu có credit): RPM 4k, TPM 4M, RPD 150k — ~20-25 phút
- Bottleneck chính: local render (PyMuPDF→JPEG) + network, không phải API rate limit
- Paid tier cho phép 8 workers concurrent

## Input Rendering
- PyMuPDF (fitz) render trực tiếp từng trang → JPEG, không cần split PDF
- Không cần Poppler (thay thế pdf2image trên Windows)

## Shared Config
- `project_config.py` — DRY paths, tất cả scripts import chung

## Railway (Track 006)
- **Plan**: Hobby ($5/mo)
- **CLI**: v4.10.0 (đã cài)
- **pgvector**: Deploy bằng one-click template (https://railway.com/deploy/pgvector-latest)
- **Connection**: `DATABASE_URL` trong `.env` (đã gitignored)
- **pgvector limits**: vector type max 2000 dims, dùng 768
- **Best practice**: HNSW index tạo SAU khi có data (không tạo trên bảng trống)

## Database Packages (Track 006)
- sqlalchemy>=2.0.0, alembic>=1.13.0, psycopg2-binary>=2.9.0, pgvector>=0.3.0