# Contract-First Framework (CFW)

> **Version**: 1.0.0 | **Date**: 2026-04-16
> Framework cho solo dev — từ PM đến tester — để tạo, lưu và sync contracts.

---

## Nguyên tắc cốt lõi

1. **Contract là nguồn sự thật duy nhất** — không phải code, không phải docs rời
2. **Không đọc codebase để biết API shape** — đọc contract
3. **Breaking change phải được ghi lại** — trước khi code, không phải sau
4. **Existing code**: capture-first → design-first cho track mới

---

## Hai workflow

### A — Capture Workflow (cho code đã tồn tại)

```
1. Export OpenAPI từ FastAPI → so sánh với contract hiện có
2. Ghi vào docs/contracts/api/<feature>.yaml
3. Update _registry.md
```

**Lệnh:**
```bash
make capture-contracts
# hoặc thủ công:
curl http://localhost:8000/openapi.json | python scripts/contracts/capture.py
```

---

### B — Design-First Workflow (cho track mới, sau khi capture xong)

```
brainstorm-track
  └── Bước cuối: viết contract_delta.md trong track folder
        → draft API endpoints (method + path + request/response shape)
        → flag breaking changes nếu có

planner-track
  └── Review contract_delta.md
  └── Update docs/contracts/api/<feature>.yaml TRƯỚC khi viết code
  └── Chạy: make sync-types (generate TS types từ OpenAPI)

[Dev phase]
  └── Backend: implement theo spec (không ngược lại)
  └── Frontend: dùng generated types từ frontend/src/types/_generated/

done-checklist (gate bắt buộc)
  └── [ ] Contract đã update trong docs/contracts/
  └── [ ] make sync-types đã chạy, types commit cùng PR
  └── [ ] _registry.md đã cập nhật version + date
  └── [ ] Breaking changes đã ghi vào _registry.md Breaking Change Log
```

---

## Cấu trúc thư mục

```
docs/contracts/
  FRAMEWORK.md              ← file này (how-to)
  _registry.md              ← index tất cả contracts + breaking changes
  api/
    <feature>.yaml          ← OpenAPI spec (aggregated source of truth)
  engine/
    <feature>.md            ← Computation contract (input/output/invariants)

conductor/tracks/<id>/
  contract_delta.md         ← Track-level: thêm/sửa gì trong track này
                               (chỉ ghi diff, không duplicate nội dung)

frontend/src/types/
  _generated/               ← Auto-generated từ OpenAPI (KHÔNG sửa tay)
    <feature>.ts
```

---

## Tooling

### `make capture-contracts`
Export OpenAPI từ backend đang chạy, save vào `docs/contracts/api/<feature>.yaml`.

```bash
# Yêu cầu: backend đang chạy ở localhost:8000
python scripts/contracts/capture.py
```

### `make sync-types`
Generate TypeScript types từ OpenAPI spec.

```bash
# Yêu cầu: npx openapi-typescript đã install
npx openapi-typescript docs/contracts/api/<feature>.yaml -o frontend/src/types/_generated/<feature>.ts
```

### `make validate-contracts`
So sánh OpenAPI live với spec đã commit — báo lỗi nếu khác nhau.

```bash
python scripts/contracts/validate.py
```

---

## Contract Delta Template

Mỗi track có `contract_delta.md` với format:

```markdown
# Contract Delta — Track <ID>: <Name>

## API Changes

### Added
- `POST /<prefix>/<new-endpoint>` — mô tả ngắn
  - Request: `{ field: type }`
  - Response: `{ field: type }`

### Modified
- `GET /<prefix>/<endpoint>` — thêm field `xyz: string` vào response
  - ⚠️ Breaking: không (field mới, additive)

### Removed
- *(none)*

## Engine Contract Changes

- *(none)*

## Breaking Changes

- *(none)* / hoặc mô tả + migration path

## Linked contracts
- Updates: `docs/contracts/api/<feature>.yaml` (version bump: 1.x.x → 1.x+1.x)
```

---

## Quy tắc versioning

API Contract dùng **Semantic Versioning**:
- `PATCH` (1.0.**x**): thêm field mới vào response (additive, non-breaking)
- `MINOR` (1.**x**.0): thêm endpoint mới
- `MAJOR` (**x**.0.0): thay đổi breaking (xóa field, đổi type, đổi path)

---

## Tích hợp với Conductor

| Skill | Contract touchpoint |
|-------|-------------------|
| `/brainstorm-track` | Draft `contract_delta.md` ở bước cuối |
| `/planner-track` | Review delta, update `docs/contracts/api/*.yaml` |
| `/done-checklist` | Gate: verify contract + types đã sync |
| `/update-knowledge` | Không cần — contract tự là knowledge |
