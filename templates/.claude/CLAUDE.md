---
priority: highest
always_load: true
---

# {{PROJECT_NAME}}

## Project
- **Name**: {{PROJECT_NAME}}
- **Stack**: {{PROJECT_STACK}}
- **Deploy**: Frontend -> {{FRONTEND_DEPLOY}} | Backend -> {{BACKEND_DEPLOY}}
- **Full stack**: `{{FULL_STACK_DOC_PATH}}`

## Rules
- **NEVER** auto-commit or auto-push
- Read files before modifying
- Verify before claiming done
- Use skills from `.claude/skills/`
- Parallelize reads when useful

## Communication
- User: **{{USER_NAME}}** | Assistant: **{{ASSISTANT_NAME}}**
- Direct, concise
- Thinking phải bằng tiếng Việt

## Workflow
- Tracks: `conductor/tracks/` | Status: `conductor/tracks.md`
- Workflow standard: `conductor/workflow.md`
- Skills: `.claude/skills/`
- Project memory: `docs/memory/MEMORY.md`
