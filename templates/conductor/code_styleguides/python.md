# Python Code Style Guide

For FastAPI backends, Pydantic models, SQLAlchemy ORM, and standalone Python scripts.

## Formatting

- Indentation: **4 spaces** (no tabs)
- Line limit: **100 characters**
- Formatter: `black` (auto-format before commit)
- Linter: `ruff` or `pylint`

## Type Annotations

- **Required** on all function signatures (args + return type).
- Use `Optional[X]` or `X | None` for nullable. Prefer `X | None` (Python 3.10+).
- Use `list[X]`, `dict[K, V]` (lowercase generics, Python 3.9+). Not `List`, `Dict`.
- `Any` is forbidden unless wrapping external untyped libs — add a `# noqa: ANN401` comment.

```python
# Good
def get_user(user_id: int) -> User | None:
    ...

# Bad
def get_user(user_id, user=None):
    ...
```

## Naming

| Element | Convention | Example |
|---|---|---|
| Functions / variables | `snake_case` | `get_user_by_id` |
| Classes | `PascalCase` | `UserResponse` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Private | leading `_` | `_build_query` |
| Files / modules | `snake_case` | `user_service.py` |

## FastAPI Patterns

- **Router prefix** declared in `router = APIRouter(prefix="/users", tags=["users"])`.
- **Always** set `response_model=Schema` on route decorators.
- Dependency injection via `Depends()` — never call service functions directly in routes.
- Async routes (`async def`) for all I/O-bound handlers.

```python
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    user = await user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Pydantic Models

- Input schemas: `XCreate`, `XUpdate`
- Output schemas: `XResponse`, `XDetail`
- Use `model_config = ConfigDict(from_attributes=True)` for ORM compat.
- Never expose raw ORM models to API responses.

## SQLAlchemy / Database

- Use `select()` + `session.execute()` (SQLAlchemy 2.x style). Not `session.query()`.
- Eager-load relations with `selectinload()` when needed. Never rely on lazy load in async context.
- Migrations via `alembic`. Never modify DB schema by hand.
- Index columns used in `WHERE` / `JOIN` / `ORDER BY`.

## Error Handling

- Raise `HTTPException` with explicit `status_code` and `detail` in route layer.
- Service layer raises domain exceptions (e.g., `ValueError`, `PermissionError`).
- Never `except Exception: pass`. Log + re-raise minimum.

```python
# Good
try:
    result = await some_service.call()
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e)) from e
```

## Scripts & CLI

- All executable scripts: wrap logic in `def main() -> None:` and call via `if __name__ == "__main__": main()`.
- Use `argparse` or `typer` for CLI args. No positional sys.argv parsing.
- Print progress to stderr (`sys.stderr`), final output to stdout.

## Tests

- File: `test_<module>.py`, function: `test_<scenario>_<expected>`.
- Use `pytest`. Async tests with `pytest-asyncio`.
- No mocking the database in integration tests — use a real test DB.
- One assertion per logical scenario (multiple asserts OK if testing one concept).
