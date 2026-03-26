#!/usr/bin/env python3
"""
Initialize track structure for module refactoring.

Usage:
    python init_refactor_track.py --track-id 049 --module "User Management" --priority P1
"""

import argparse
import os
from pathlib import Path
from datetime import date


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    return text.lower().replace(" ", "-").replace("_", "-")


def create_refactor_track(track_id: str, module: str, priority: str):
    """Create refactor track folder structure and template files."""

    # Create track folder
    slug = slugify(module)
    track_folder = Path(f"conductor/tracks/{track_id}-refactor-{slug}")
    track_folder.mkdir(parents=True, exist_ok=True)

    print(f"✓ Created refactor track folder: {track_folder}")

    # Priority emoji
    priority_emoji = {
        "P0": "🔴",
        "P1": "🟠",
        "P2": "🟡",
        "P3": "⚪"
    }.get(priority, "⚪")

    # Create README.md
    readme_content = f"""# Track {track_id}: Refactor {module}

**Status**: 🔄 In Progress
**Created**: {date.today().isoformat()}
**Type**: Module Refactoring
**Priority**: {priority_emoji} {priority}

## Refactoring Phases

- [ ] Phase 1: Root Cause Analysis (RCA)
- [ ] Phase 2: Re-Architecture (if needed)
- [ ] Phase 3: Refactoring Plan
- [ ] Phase 4: Backend Refactoring
- [ ] Phase 5: Frontend Refactoring
- [ ] Phase 6: Quality Assurance & Verification

## Files

- [README.md](./README.md) - This file
- [RCA.md](./RCA.md) - Root Cause Analysis
- [ARCHITECTURE_REFACTOR.md](./ARCHITECTURE_REFACTOR.md) - Re-architecture design (if needed)
- [REFACTORING_PLAN.md](./REFACTORING_PLAN.md) - Detailed refactoring plan
- [QA_REPORT.md](./QA_REPORT.md) - Quality assurance report

## References

- [WORKFLOW_STANDARD.md](../../.claude/docs/WORKFLOW_STANDARD.md)
- [refactor-workflow skill](../../.claude/skills/refactor-workflow/SKILL.md)
"""

    (track_folder / "README.md").write_text(readme_content, encoding="utf-8")
    print(f"✓ Created README.md")

    # Create template files
    templates = {
        "RCA.md": f"""# Root Cause Analysis - {module}

## Current State

### What is Working
- [List features/code that work correctly]

### What is Broken
- [List issues, bugs, inconsistencies]

---

## Issues Identified

### P0: Critical Issues (Blocking)

#### Issue 1: [Title]
- **Symptom**: [What user/developer sees]
- **Root Cause**: [Technical reason]
- **Impact**: [Business/user/developer impact]
- **Example**:
  ```python
  # Code snippet showing the problem
  ```

### P1: High Priority (Performance/Consistency)

[Same format as P0]

### P2: Medium Priority (Code Quality)

[Same format as P0]

### P3: Low Priority (Nice to have)

[Same format as P0]

---

## Root Causes Analysis

### Architecture Issues
- [e.g., Tight coupling between X and Y]
- [Missing abstraction layer]

### Code Quality Issues
- **Duplication**: [List repeated code blocks]
- **Complexity**: [High cyclomatic complexity functions]
- **No error handling**: [Critical paths without try/catch]

### Performance Issues
- N+1 queries in [endpoint]
- No pagination on large datasets
- Missing database indexes on [columns]

### Consistency Issues
- Inconsistent naming conventions
- Mixed patterns (some use Service, some don't)
- Data integrity issues

---

## Recommended Approach

### Option 1: Incremental Refactoring ⭐ RECOMMENDED
**Pros**:
- Low risk
- Can ship improvements incrementally
- Backward compatible
- Can rollback at any step

**Cons**:
- Slower
- May leave some tech debt initially

**When**: Most cases, especially production modules

---

### Option 2: Rewrite from Scratch
**Pros**:
- Clean slate
- Apply best practices from start
- Modern patterns

**Cons**:
- High risk
- Long time to ship
- May introduce new bugs
- Feature parity challenge

**When**: Module is fundamentally broken, few users

---

### Option 3: Hybrid
**Pros**:
- Balance risk and improvement
- Focus effort on critical paths

**Cons**:
- Need careful planning
- Inconsistency during transition

**When**: Some parts work well, others don't

---

## Chosen Approach: [Option X]

**Rationale**:
[Explain why this approach makes sense for this specific situation]

---

## Migration Strategy

1. [Step 1]
2. [Step 2]
3. [...]

---

## Success Criteria

- [ ] All P0 issues resolved
- [ ] All P1 issues resolved
- [ ] Code quality metrics improved
- [ ] Performance benchmarks met
- [ ] No regression in existing features

---

## Timeline Estimate

- RCA: 2 hours
- Re-architecture: 3 hours (if needed)
- Implementation: 10-15 hours
- Testing: 3 hours
- **Total**: 18-23 hours
""",

        "REFACTORING_PLAN.md": f"""# Refactoring Plan - {module}

## Preparation

### Backup & Safety
- [ ] Create git tag: `refactor-{slugify(module)}-backup`
- [ ] Create feature flag: `refactor_{slugify(module)}`
- [ ] Write regression test suite

### Baseline Metrics
```bash
# Backend
cd backend && pytest tests/test_{slugify(module)}.py --cov

# Frontend
cd frontend && npm run lint && npm run type-check
```

---

## Incremental Steps

### Step 1: [Title]

**Files to modify**:
- `backend/...`
- `frontend/...`

**Changes**:
```python
# Before
[current code]

# After
[proposed code]
```

**Verification**:
- [ ] Tests pass
- [ ] Integrity check PASS
- [ ] Manual testing: [specific scenarios]

**Rollback**: `git revert [commit]`

---

### Step 2: [Title]

[Same format as Step 1]

---

### Step 3: [Title]

[Same format as Step 1]

---

## Testing Strategy

### Regression Tests
- [ ] All existing features work
- [ ] No breaking changes

### Performance Benchmarks
**Before**:
- API response time: [X ms]
- Database queries: [N queries]

**After (Target)**:
- API response time: < [Y ms]
- Database queries: < [M queries]

### Manual Testing Checklist
- [ ] Test scenario 1
- [ ] Test scenario 2
- [ ] Test scenario 3

---

## Rollback Plan

If step X fails:
1. `git revert [commit]`
2. Turn off feature flag
3. Deploy previous version
4. Investigate issue
5. Fix and retry

---

## Timeline Estimate

| Step | Estimate | Dependencies |
|------|----------|--------------|
| Step 1 | 2 hours | None |
| Step 2 | 3 hours | Step 1 complete |
| Step 3 | 2 hours | Step 2 complete |
| **Total** | 7 hours | - |
"""
    }

    for filename, content in templates.items():
        (track_folder / filename).write_text(content, encoding="utf-8")
        print(f"✓ Created {filename}")

    # Create .phase file
    (track_folder / ".phase").write_text("phase-1-rca", encoding="utf-8")
    print(f"✓ Created .phase (current: phase-1-rca)")

    print(f"\n✅ Refactor track {track_id} initialized successfully!")
    print(f"\nNext steps:")
    print(f"1. Update conductor/tracks.md to add this track")
    print(f"2. Start with Phase 1: Root Cause Analysis")
    print(f"3. Invoke /refactoring-expert to analyze code")

    return track_folder


def main():
    parser = argparse.ArgumentParser(description="Initialize refactor track")
    parser.add_argument("--track-id", required=True, help="Track ID (e.g., 049)")
    parser.add_argument("--module", required=True, help="Module name to refactor (e.g., 'User Management')")
    parser.add_argument(
        "--priority",
        choices=["P0", "P1", "P2", "P3"],
        default="P2",
        help="Priority: P0=Critical, P1=High, P2=Medium, P3=Low"
    )

    args = parser.parse_args()

    create_refactor_track(args.track_id, args.module, args.priority)


if __name__ == "__main__":
    main()
