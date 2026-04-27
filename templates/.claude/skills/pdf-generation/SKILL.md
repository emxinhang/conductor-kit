---
name: pdf-generation
description: Chuẩn hóa pattern WeasyPrint + Jinja2 cho PDF generation trong TMS-2026 — itinerary proposal và invoice. Dùng khi thêm tính năng export PDF mới hoặc sửa template PDF hiện có.
allowed-tools:
  - Bash
  - Read
---

# PDF Generation — WeasyPrint + Jinja2 Pattern (TMS-2026)

**Stack:** WeasyPrint + Jinja2Templates (FastAPI) + Cloudflare R2 (assets)  
**Hai service PDF hiện có:**
- `app/services/pdf_service.py` — Itinerary Proposal (FR/IT/EN)
- `app/services/invoice_pdf_service.py` — Invoice/Facture (FR/IT/EN)

---

## 1. Kiến trúc tổng quan

```
FastAPI Route
    ↓
PDFService.generate_*_pdf(id)
    ↓
_fetch_data()          → SQLAlchemy async query với eager loading
    ↓
_prepare_context()     → Dict với data, labels, helper functions
    ↓
_render_html()         → Jinja2Templates.get_template().render(context)
    ↓
HTML(string=html, base_url=BASE_DIR).write_pdf(pdf_file)
    ↓
StreamingResponse(media_type="application/pdf")
```

---

## 2. Tạo PDFService mới

### 2a. Service file (`app/services/<name>_pdf_service.py`)

```python
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from weasyprint import HTML
from io import BytesIO
from app.core.config import settings
import logging


class MyEntityPDFService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.templates = Jinja2Templates(directory="app/templates")
        self.logger = logging.getLogger(__name__)

    async def generate_pdf(self, entity_id: int) -> StreamingResponse:
        entity = await self._fetch_data(entity_id)
        if not entity:
            raise ValueError(f"Entity {entity_id} not found")
        
        context = await self._prepare_context(entity)
        html_content = self._render_html(context)
        return self._build_response(html_content, entity_id)

    async def _fetch_data(self, entity_id: int):
        """Eager load tất cả relations cần dùng trong template."""
        result = await self.db.execute(
            select(MyEntity)
            .where(MyEntity.id == entity_id)
            .options(
                joinedload(MyEntity.owner),
                selectinload(MyEntity.items),
            )
        )
        return result.unique().scalar_one_or_none()

    async def _prepare_context(self, entity) -> dict:
        lang = entity.language or "fr"
        return {
            "entity": entity,
            "lang": lang,
            "labels": self._get_labels(lang),
            "format_currency": self._format_currency,
            "format_date": self._format_date,
        }

    def _render_html(self, context: dict) -> str:
        template = self.templates.get_template("my_entity/index.html")
        return template.render(context)

    def _build_response(self, html_content: str, entity_id: int) -> StreamingResponse:
        pdf_file = BytesIO()
        HTML(string=html_content, base_url=str(settings.BASE_DIR)).write_pdf(pdf_file)
        pdf_file.seek(0)
        return StreamingResponse(
            pdf_file,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=doc_{entity_id}.pdf"}
        )
```

### 2b. Template (`app/templates/<name>/index.html`)

```html
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
  <meta charset="UTF-8">
  <style>
    /* CSS cho WeasyPrint — không dùng flexbox phức tạp */
    @page {
      size: A4;
      margin: 20mm 15mm;
    }
    body { font-family: 'DejaVu Sans', sans-serif; font-size: 10pt; }
    .page-break { page-break-before: always; }
    
    /* Images — PHẢI dùng absolute path hoặc base64 */
    img { max-width: 100%; }
  </style>
</head>
<body>
  <h1>{{ labels.title }}</h1>
  {% for item in entity.items %}
    <div>{{ item.name }}</div>
  {% endfor %}
</body>
</html>
```

---

## 3. Cấu trúc thư mục

```
backend/
├── app/
│   ├── services/
│   │   ├── pdf_service.py           ← Itinerary PDF
│   │   └── invoice_pdf_service.py   ← Invoice PDF
│   └── templates/
│       ├── proposal/
│       │   └── index.html
│       └── invoice/
│           └── invoice.html
```

---

## 4. i18n Labels Pattern

**Không hardcode text trong template.** Dùng label dict theo ngôn ngữ:

```python
# app/i18n/invoice/fr.json
{
  "title": "FACTURE",
  "date": "Date",
  "total": "Total TTC"
}

# Trong service:
def _get_labels(self, lang: str) -> dict:
    import json, os
    file_path = os.path.join(settings.BASE_DIR, "app", "i18n", "my_entity", f"{lang}.json")
    if not os.path.exists(file_path):
        file_path = file_path.replace(f"/{lang}.json", "/fr.json")  # fallback FR
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)
```

---

## 5. Images trong WeasyPrint

**WeasyPrint resolve image URL theo `base_url`.** Dùng đúng cách:

```python
# ✅ base_url = thư mục gốc backend
HTML(string=html, base_url=str(settings.BASE_DIR)).write_pdf(pdf_file)

# ✅ Trong template: relative path từ BASE_DIR
<img src="app/static/logo.png">

# ✅ Remote URL (Cloudflare R2) — hoạt động nếu server có internet
<img src="https://pub-xxx.r2.dev/tms-2026/uploads/logo.png">

# ❌ Không dùng data URI quá lớn (>1MB) — làm chậm render
```

**Railway production:** Server có internet → R2 URLs hoạt động bình thường.

---

## 6. CSS WeasyPrint — Gotchas

```css
/* ✅ Supported */
@page { size: A4; margin: 20mm; }
page-break-before: always;
page-break-inside: avoid;
float: left/right;
position: absolute/relative;

/* ⚠️ Hạn chế */
flexbox: hỗ trợ cơ bản, tránh flex-wrap phức tạp
grid: hỗ trợ một phần, test kỹ
box-shadow: không render

/* ❌ Không dùng */
position: fixed (chỉ dùng cho @page margin boxes)
CSS variables (--var) không được hỗ trợ đầy đủ
```

---

## 7. API Endpoint Pattern

```python
# app/api/v1/my_entity.py
@router.get("/{entity_id}/pdf")
async def export_pdf(
    entity_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MyEntityPDFService(db)
    try:
        return await service.generate_pdf(entity_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"PDF generation failed for entity {entity_id}: {e}")
        raise HTTPException(status_code=500, detail="PDF generation failed")
```

---

## 8. Test PDF locally

```bash
cd backend

# Chạy server
uvicorn app.main:app --reload

# Test bằng curl — lưu thành file
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/my-entity/1/pdf \
  --output test_output.pdf

# Mở để kiểm tra
start test_output.pdf   # Windows
```

---

## 9. Checklist trước khi done

- [ ] `_fetch_data()` eager load đủ relations (không có lazy load trong async context)
- [ ] `downgrade()` migration có nếu thêm model field
- [ ] Template dùng labels dict, không hardcode text
- [ ] Image URLs hoạt động trên Railway (test với remote URL)
- [ ] `base_url=str(settings.BASE_DIR)` được set trong `HTML()`
- [ ] API endpoint có try/except, trả 404 khi not found, 500 khi PDF lỗi
- [ ] Filename trong `Content-Disposition` có ý nghĩa (`Invoice_VT-2026-001.pdf`)
