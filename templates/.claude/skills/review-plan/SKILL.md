---
name: review-plan
description: Dung skill review-plan de kiem tra IMPLEMENTATION_PLAN.md truoc khi bat dau code - phat hien bugs, race conditions, API contract issues va data model mismatches. Su dung sau /planner-track va TRUOC khi implement.
---

# Review Plan

Review IMPLEMENTATION_PLAN.md theo checklist 5 categories truoc khi viet bat ky dong code nao. Muc tieu: phat hien bugs o plan-level (roi hon bug-level) de tranh vong loop "implement - bug - refactor".

## When to Use

Dung ngay sau khi `/planner-track` tao ra `IMPLEMENTATION_PLAN.md`, truoc khi bat dau Phase 4 (Backend) hoac Phase 5 (Frontend).

## Review Process

### Buoc 1: Doc Plan

Doc toan bo `IMPLEMENTATION_PLAN.md` trong track folder. Dam bao hieu ro:
- So luong files can tao/sua
- Thu tu phases
- Dependencies giua cac buoc

### Buoc 2: Ap dung 5-Category Checklist

#### Category 1: API Contract Issues
- [ ] Moi API call co dung method (GET/POST/PATCH/DELETE)?
- [ ] Response type co match voi TypeScript type da dinh nghia?
- [ ] Co goi nhieu API calls doc lap cho 1 action khong? (nen batch thanh 1)
- [ ] Params optional/required co dung khong?

**TMS-2026 gotcha**: Neu plan co nhieu `handleUpdate()` calls lien tiep cho 1 action, nen batch vao 1 `updateItem()`.

#### Category 2: State & Async Race Conditions
- [ ] Co truong hop "await A - dung ket qua cua A ngay" nhung A chua return?
- [ ] Local state (useState) co duoc update ngay truoc khi goi API khong (UX)?
- [ ] Co `useEffect` nao co the trigger vo han (missing deps, stale closure)?
- [ ] Store actions co fetch lai sau khi mutate, hay chi update local?

**TMS-2026 gotcha**: `reorderItems` trong quoteStore co goi `fetchQuote` sau khi call API - dam bao cac plan khac dua vao behavior nay la dung.

#### Category 3: Data Model Mismatches
- [ ] Moi field duoc plan su dung co ton tai trong TypeScript interface?
- [ ] Moi field duoc plan su dung co ton tai trong Pydantic schema?
- [ ] Foreign key relationships co duoc selectinload/joined load?
- [ ] Co field nao trong PRD nhung khong co trong actual model?

**TMS-2026 gotcha**: Kiem tra `QuoteItem` vs `QuoteTemplate` - co nhung fields chi co o template (vi du `unit`) nhung khong o item.

#### Category 4: Backend FastAPI Patterns
- [ ] Moi router co `response_model=` khong? (REQUIRED - else computed_field bi break)
- [ ] Async relations co dung `selectinload` khong? (else MissingGreenlet)
- [ ] Datetime fields co `@field_serializer` append 'Z' khong?
- [ ] New migration file can duoc commit truoc khi Railway deploy?

#### Category 5: Frontend React Patterns
- [ ] `useState(initialData)` co can `useEffect` de sync khi prop thay doi?
- [ ] `React.memo` comparator co can update neu them props moi?
- [ ] Global hotkeys co kiem tra `document.activeElement` truoc?
- [ ] Components dung `import` static hay dynamic? (tranh import trong callbacks)

### Buoc 3: Check Dependencies & Order

- [ ] Backend Phase hoan thanh truoc khi bat dau Frontend Phase?
- [ ] Migration chay truoc khi test API?
- [ ] Co circular dependency giua cac files khong?

### Buoc 4: Flag & Fix

Voi moi van de tim thay:
1. Phan loai: Bug | UX Issue | Data Mismatch | Pattern Violation
2. Cap do: Critical (se crash/break) | Important (UX bad) | Minor (code smell)
3. De xuat fix cu the vao IMPLEMENTATION_PLAN.md

### Buoc 5: Update Plan

- Cap nhat IMPLEMENTATION_PLAN.md voi cac fixes
- Them ghi chu vao checklist items lien quan
- Bao cao ket qua: "X issues found, Y fixed"

## Output Format

```
## Review Results - IMPLEMENTATION_PLAN.md

### Issues Found: X

| # | Category | Type | Description | Fix |
|---|----------|------|-------------|-----|
| 1 | API Contract | Critical | ... | ... |
| 2 | State | Important | ... | ... |

### Confirmations (OK)
- [x] ...

### Plan Updated: Yes/No
```

## Notes

- Khong review code (chua co) - review plan document
- Tap trung vao "se xay ra gi khi implement dung plan nay?"
- Uu tien Critical issues truoc, sau do Important
- Neu plan qua ngan/thieu chi tiet - flag de planner-track lam lai