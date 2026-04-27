# TMS-2026 Skills

Optimized skills collection for TMS-2026 (Tour Management System) - React 19 + FastAPI + PostgreSQL.

**Last optimized:** 2026-03-03 | **Total skills:** 53 (pruned from 80)

For more information, check out:
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Equipping agents for the real world with Agent Skills](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## Quick Start

See **[SKILLS_CATALOG_VI.md](./SKILLS_CATALOG_VI.md)** for complete skills catalog with Vietnamese descriptions organized by category.

## Skills Organization

Skills are grouped into these categories:
- **Core Project Management** (conductor, module-workflow, planner-track, etc.)
- **Frontend Development** (React 19, shadcn-ui, Tailwind CSS)
- **Backend Development** (FastAPI, PostgreSQL, zero-loop-dev)
- **Debugging & QA** (systematic debugging, code review, verification)
- **Problem Solving** (collision-zone thinking, inversion, scale-game, etc.)
- **Documentation & Research** (technical writing, requirements analysis, etc.)
- **ATu-specific** (custom skills for user ATu)

## Skills Pruned (27 removed)

Removed skills unrelated to TMS-2026 stack (React 19 + FastAPI + PostgreSQL + Railway + Vercel):

**AI/ML Providers:** gemini-audio, gemini-document-processing, gemini-image-gen, gemini-video-understanding, gemini-vision, google-adk-python (Google AI)

**Frontend:** nextjs (using Vite React instead)

**Cloud:** cloudflare, cloudflare-browser-rendering, cloudflare-workers, gcloud (using Vercel + Railway)

**Infrastructure:** docker, turborepo

**Databases:** mongodb (using PostgreSQL)

**Tools:** chrome-devtools

**Multimedia:** ffmpeg, imagemagick

**E-commerce:** shopify

**Document Processing:** document-skills/ (4 skills - Word, PDF, PowerPoint, Excel)

**Other:** better-auth (using OAuth 2.1 + JWT), canvas-design, remix-icon, problem-solving (using individual skills), template-skill, deep-research-agent

## How to Use Skills

In Claude Code, simply mention the skill name and Claude will load it:

```
Use frontend-standard-v1 to create a new module
Use zero-loop-dev for creating a new backend entity
Run debugging-systematic-debugging when encountering a bug
Use shadcn-ui + tailwindcss to build the UI component
```

## Using Skills in This Project

**For new features:**
```
/module-workflow     # Start new module from Requirements → QA
/planner-track       # Create Implementation Plan after requirements finalized
```

**For debugging:**
```
/debugging-systematic-debugging    # 4-phase debugging framework
/code-review                        # Before marking tasks as Done
/debugging-verification-before-completion  # Final verification before PR
```

**For frontend development:**
```
/frontend-standard-v1      # TMS-2026 frontend patterns
/shadcn-ui                 # Build components
/tailwindcss               # Styling
/frontend-qa-gatekeeper    # QA verification
```

**For backend development:**
```
/zero-loop-dev             # Backend scaffolding
/postgresql-psql           # Database management
/backend-development       # FastAPI patterns
/qa-verify-expert          # API contract verification
```

## Project Memory Integration

Skills integrate with project memory for knowledge persistence:
- `update-knowledge` saves learnings at session end
- `new-conversation` loads context at session start
- See [docs/memory/MEMORY.md](../../docs/memory/MEMORY.md) for the memory index and `docs/memory/` for persisted learnings
