# TypeScript / React Code Style Guide

For React 19 + Vite frontends using TanStack Router, TanStack Query, and MUI v7.

## Formatting

- Indentation: **2 spaces**
- Line limit: **100 characters**
- Formatter: `prettier` (auto-format on save)
- Linter: `eslint` with TypeScript plugin

## TypeScript Rules

- **No `any`**. Use `unknown` + type narrowing if type is uncertain.
- **No type assertions** (`as X`) unless wrapping untyped third-party code — add comment.
- **No non-null assertions** (`!`) except in tests.
- Prefer `interface` for object shapes, `type` for unions/intersections.
- Explicit return types on all exported functions.

```typescript
// Good
function getUser(id: number): Promise<User | null> { ... }

// Bad
const getUser = async (id: any) => { ... }
```

## Naming

| Element | Convention | Example |
|---|---|---|
| Components | `PascalCase` | `UserCard` |
| Hooks | `camelCase` with `use` prefix | `useUserData` |
| Functions / variables | `camelCase` | `fetchUser` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_PAGE_SIZE` |
| Types / Interfaces | `PascalCase` | `UserResponse` |
| Files (components) | `PascalCase.tsx` | `UserCard.tsx` |
| Files (utils/hooks) | `camelCase.ts` | `useUserData.ts` |

## Module Exports

- **Named exports only**. No default exports.
- Exception: route files (TanStack Router requires default export for `createFileRoute`).

```typescript
// Good
export function UserCard({ user }: UserCardProps) { ... }

// Bad
export default function UserCard() { ... }
```

## React Component Rules

- Functional components only. No class components.
- Props interface defined above the component: `interface UserCardProps { ... }`.
- Destructure props in function signature.
- `key` prop: always use stable IDs, never array index.

```typescript
interface UserCardProps {
  user: User
  onSelect: (id: number) => void
}

export function UserCard({ user, onSelect }: UserCardProps) {
  return (...)
}
```

## Data Fetching — TanStack Query

- Use `useSuspenseQuery` for data that must exist (throw on error/loading via Suspense boundary).
- Use `useQuery` when loading/error state is handled manually.
- Query keys: `[entity, action, params]` — e.g., `['users', 'list', { page }]`.
- Mutations via `useMutation` with `onSuccess` → `queryClient.invalidateQueries`.

```typescript
// Good — Suspense-ready
const { data: users } = useSuspenseQuery({
  queryKey: ['users', 'list', filters],
  queryFn: () => userApi.list(filters),
})
```

## Routing — TanStack Router

- One file per route in `src/routes/`.
- Route params typed via `Route.useParams()`. Never use `useParams()` from React Router.
- Loaders for data that must be available before render.
- `createFileRoute('...')` at the top of every route file.

## Styling — MUI v7

- Use `sx` prop for one-off styles. `styled()` for reusable styled components.
- No inline `style={{}}` attributes — use `sx` instead.
- Spacing via theme units (`sx={{ mt: 2 }}` not `sx={{ marginTop: '16px' }}`).
- Colors via theme tokens (`color: 'text.secondary'`) not hardcoded hex.

```typescript
// Good
<Box sx={{ display: 'flex', gap: 2, mt: 1 }}>

// Bad
<Box style={{ display: 'flex', gap: '16px', marginTop: '8px' }}>
```

## State Management

- Local state: `useState` / `useReducer`.
- Server state: TanStack Query (do not duplicate in `useState`).
- Global UI state: context or Zustand (only when >2 components need it).
- Never store derived data in state — compute from existing state/query data.

## Error Handling

- Wrap async operations in `try/catch`. Log errors, show user-facing message via toast/snackbar.
- Use `ErrorBoundary` at route level to catch render errors.
- API errors: check `response.ok` before parsing JSON.

## Performance

- `React.lazy()` + `Suspense` for route-level code splitting.
- `useMemo` / `useCallback` only when profiling confirms benefit — not preemptively.
- Avoid anonymous functions in JSX props on hot paths (they recreate every render).

## Tests

- File: `ComponentName.test.tsx`, test: `it('should ...')`.
- Use `@testing-library/react`. No Enzyme.
- Test user behavior, not implementation details.
- Mock API calls at the network level (`msw`), not at the module level.
