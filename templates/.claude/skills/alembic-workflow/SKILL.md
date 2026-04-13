---
name: alembic-workflow
description: Chuẩn hóa quy trình Alembic migration cho TMS-2026 — naming convention, viết downgrade() reversible, test trước deploy, xử lý data migration. Dùng mỗi khi thêm/sửa model database.
allowed-tools:
  - Bash
  - Read
---

# Alembic Workflow — Chuẩn hóa Migration TMS-2026

**Stack:** FastAPI + SQLAlchemy (async) + PostgreSQL 16 + Alembic  
**Backend dir:** `T:/01-code/tms-2026/backend/`

---

## 1. Khi nào cần migration?

- Thêm/xóa/đổi tên column trong Model
- Thêm/xóa table (Model mới)
- Thêm index, unique constraint, foreign key
- Thay đổi enum values
- **Không cần:** Chỉ sửa Schema Pydantic, không sửa SQLAlchemy Model

---

## 2. Tạo Migration

### 2a. Auto-generate (schema migration)
```bash
cd backend
alembic revision --autogenerate -m "verb_noun_table"
```

**Naming convention — `verb_noun_table`:**
```
# ✅ Đúng
add_supplier_id_to_booking_ops_services
add_language_field_to_invoices
create_crm_contacts_table
drop_deprecated_tour_notes_table
alter_invoice_status_enum_add_cancelled

# ❌ Sai
migration_001
update_booking
fix_stuff
```

### 2b. Manual (data migration)
```bash
cd backend
alembic revision -m "backfill_supplier_category_from_type"
```
Dùng khi cần migrate data (không chỉ schema).

---

## 3. Cấu trúc Migration File chuẩn

```python
"""add_language_field_to_invoices

Revision ID: abc123def456
Revises: previous_revision_id
Create Date: 2026-04-07 10:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = 'abc123def456'
down_revision = 'previous_revision_id'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Mô tả ngắn gọn: thêm gì, tại sao
    op.add_column('invoices',
        sa.Column('language', sa.String(10), nullable=True, server_default='fr')
    )


def downgrade() -> None:
    # LUÔN CÓ — không được để pass hoặc bỏ trống
    op.drop_column('invoices', 'language')
```

### Rule bắt buộc cho `downgrade()`

| Upgrade làm gì | Downgrade phải làm |
|---|---|
| `add_column` | `drop_column` |
| `create_table` | `drop_table` |
| `drop_column` | `add_column` (với type gốc) |
| `add_constraint` | `drop_constraint` |
| `create_index` | `drop_index` |
| Alter enum | Alter enum ngược lại |

**Ngoại lệ chấp nhận được:** Data migration một chiều (backfill) — ghi comment rõ "irreversible data migration, downgrade is no-op" thay vì `pass`.

---

## 4. Data Migration Pattern

```python
def upgrade() -> None:
    # 1. Schema change trước
    op.add_column('suppliers',
        sa.Column('category', sa.String(50), nullable=True)
    )
    
    # 2. Data migration sau
    op.execute("""
        UPDATE suppliers
        SET category = CASE
            WHEN type = 'hotel' THEN 'accommodation'
            WHEN type IN ('bus', 'train') THEN 'transport'
            ELSE 'other'
        END
        WHERE category IS NULL
    """)
    
    # 3. Constraint sau khi data đã đủ (nếu cần nullable=False)
    op.alter_column('suppliers', 'category', nullable=False)


def downgrade() -> None:
    op.drop_column('suppliers', 'category')
```

---

## 5. Test Migration (WAJIB trước deploy)

```bash
cd backend

# Test upgrade
alembic upgrade head
echo "✅ upgrade pass" || echo "❌ upgrade FAILED"

# Verify schema
python -c "
from app.core.database import engine
import asyncio
from sqlalchemy import inspect, text

async def check():
    async with engine.connect() as conn:
        result = await conn.execute(text(\"SELECT column_name FROM information_schema.columns WHERE table_name='invoices'\"))
        print([r[0] for r in result])

asyncio.run(check())
"

# Test downgrade (quan trọng!)
alembic downgrade -1
echo "✅ downgrade pass" || echo "❌ downgrade FAILED"

# Upgrade lại để restore
alembic upgrade head
```

---

## 6. Enum Migration (hay gặp nhất)

PostgreSQL enum không thể drop value — chỉ add được:

```python
def upgrade() -> None:
    # Add enum value mới (PostgreSQL không rollback được việc này)
    op.execute("ALTER TYPE invoicestatus ADD VALUE IF NOT EXISTS 'cancelled'")

def downgrade() -> None:
    # ⚠️ PostgreSQL không support DROP VALUE từ enum
    # Documented irreversible — cần recreate table nếu muốn rollback thật
    pass  # ACCEPTABLE: ghi chú rõ lý do
```

---

## 7. Checklist trước khi commit migration

```bash
# Xem migration vừa tạo
alembic history | head -5
cat alembic/versions/<latest>.py
```

- [ ] Tên migration đúng convention `verb_noun_table`
- [ ] `upgrade()` có comment mô tả ngắn
- [ ] `downgrade()` không phải `pass` (trừ trường hợp documented)
- [ ] Đã test `alembic upgrade head` → pass
- [ ] Đã test `alembic downgrade -1` → pass
- [ ] Data migration dùng SQL thuần, không import Model (tránh circular)
- [ ] Không hardcode ID hay data production trong migration

---

## 8. Lỗi thường gặp

**"Can't locate revision"**
```bash
alembic history --verbose  # xem chain
alembic current            # xem DB đang ở revision nào
```

**Conflict sau khi merge branches**
```bash
alembic merge heads -m "merge_branch_a_and_b"
```

**Migration apply rồi muốn rollback khẩn cấp**
```bash
alembic downgrade -1        # 1 bước
alembic downgrade base      # về đầu (nguy hiểm!)
alembic downgrade <rev-id>  # về revision cụ thể
```
