---
name: frontend-qa-gatekeeper
description: A specialized skill to enforce Frontend UI/UX standards, Typescript integrity, and perform Automated QA for the React application before marking tasks as Done.
---

# Frontend QA Gatekeeper Skill

This skill provides a strict, automated approach to verifying the integrity of the project's Frontend layer. It ensures that UI components satisfy premium design requirements (Aesthetic First), Typescript interfaces match the backend contracts perfectly, state updates are performant (Zero-Latency), and the build process succeeds without warnings or errors.

## Core Capabilities

### 1. Typescript Integrity & Build Verification
Enforces strict type safety and a clean build.
- **Goal**: Prevent runtime crashes and React "White Screens of Death" caused by undefined properties, missing imports, or incorrect object structures.
- **Target**: Ensure `npm run build` (tsc -b && vite build) passes with ZERO linter errors and ZERO unused variable warnings.

### 2. UI/UX & Responsive Audit
Validates components against the TMS-2026 Frontend Standard (V1).
- **Goal**: Maintain the "Premium Feel" required by the application.
- **Rules Verified**:
  - Proper use of `AlertDialog` over `window.confirm`.
  - Implementation of `Combobox` over standard `text` inputs for entity selection.
  - Proper `Glassmorphism` and CSS variable usage (e.g., `bg-card`, `bg-muted/10`) for Dark Mode compatibility.
  - **Enforce Helper UI Patterns**: Bắt buộc phát hiện mã UI lặp lại/inline logic mapping màu sắc/icon và yêu cầu bóc tách thành UI Helper (`utils/`) hoặc Shared Components.
  - Responsive design checks for complex layouts like pricing tables.

### 3. State Management & Performance Checks
Verifies the efficiency of React state, especially for data-heavy views.
- **Goal**: Ensure zero-latency user experiences through optimistic updates and avoid unnecessary re-renders.
- **Rules Verified**:
  - Correct use of `onMutate` for optimistic updates in React Query.
  - Correct use of `setQueryData` vs `invalidateQueries` to avoid full refetches on simple mutations (e.g., adding an item).
  - Verifying `useCallback` and `React.memo` integration for large lists (e.g., Itinerary Days).
  - Use of Local State (`useState`) + `onBlur`/`Enter` for inline editing over firing API requests `onChange`.

## Usage

### Phase 1: Pre-Commit Build Check
Before declaring a frontend track or feature complete, always run the build compiler to catch hidden issues:
```bash
npm run build
```
*(Note: Fix all `unused variable` warnings or strict type errors before proceeding).*

### Phase 2: Component & Standard Audit
Ask CS to perform a code review on the specific `.tsx` files modified during the session:
1. "Run the `frontend-qa-gatekeeper` audit on `ItinerariesPage.tsx`."
2. CS will review the code for hardcoded strings, missing `AlertDialogs`, improper `Combobox` usage, or `any` typing.

### Phase 3: Behavior & Latency Verification (The UI Acid Test)
Ask CS to verify the interaction loop:
1. "Review the mutation logic in `DayTab.tsx` for optimistic UI updates according to the QA gatekeeper."
2. CS will check if the cache is updated locally or if it falls back to a slow, full network request unnecessarily.

## Rules of Engagement

1. **Zero-Lint Policy**: The standard is strict. A successful feature implementation is not complete if the compiler emits unused import warnings. The code must be clean.
2. **Prop Drilling vs Context/Store**: If you see more than 3 levels of prop drilling during a review, recommend a refactor to Zustand or React Context.
3. **No Silent UI Fails**: If a mutation fails (e.g., backend returns 400), the UI MUST have an `onError` handler that displays a `toast.error()`. A component without error handling fails the QA Gatekeeper.