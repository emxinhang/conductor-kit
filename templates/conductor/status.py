#!/usr/bin/env python3
"""
conductor/status.py — Conductor Dashboard

Usage:
  python conductor/status.py                              # Show dashboard
  python conductor/status.py done                         # Mark ACTIVE track as done, promote PIPELINE[0]
  python conductor/status.py next                         # Alias for done
  python conductor/status.py close <id> [agent] [note]   # Shortcut: transition <id> done
  python conductor/status.py note "..."                   # Update ACTIVE notes
  python conductor/status.py add "name"                   # Add track to BACKLOG
  python conductor/status.py transition <id> <phase> [agent] [note]
                                                          # Update track phase automatically
                                                          # phase: brainstorm | planned | dev | qa | done
                                                          # Updates: tracks.md + state.md + CHANGELOG.md + active_context.md
"""

import sys
import re
from pathlib import Path
from datetime import date

# Windows terminal UTF-8 fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STATE      = Path(__file__).parent / "state.md"
TRACKS     = Path(__file__).parent / "tracks.md"
CONTEXT    = Path(__file__).parent.parent / "docs/memory/00_active_context.md"
TRACKS_DIR = Path(__file__).parent / "tracks"
W = 80  # box width

PHASE_MAP = {
    "brainstorm": "[📋 Brainstorm]",  # has PRD/spec only, no plan yet
    "planned":    "[📅 Planned]",     # has IMPLEMENTATION_PLAN.md
    "dev":        "[💻 Dev]",         # in active development
    "qa":         "[🧪 QA]",          # verifying / smoke test
    "done":       "✅ Completed",     # released & wrapped up
}

PHASE_ICON = {
    "brainstorm": "📋",
    "planned":    "📅",
    "dev":        "💻",
    "qa":         "🧪",
    "done":       "✅",
}

PHASE_LABEL = {
    "brainstorm": "Brainstorm",
    "planned":    "Planned",
    "dev":        "Dev",
    "qa":         "QA",
    "done":       "Done",
}


# ── Box drawing ────────────────────────────────────────

def top(): return "╔" + "═" * W + "╗"
def mid(): return "╠" + "═" * W + "╣"
def bot(): return "╚" + "═" * W + "╝"

def row(text=""):
    text = str(text)
    max_w = W - 4
    if len(text) <= max_w:
        return f"║  {text:<{max_w}}  ║"

    # Simple wrap: split by space or just chunk it
    lines = []
    while len(text) > max_w:
        # Try to break at space
        break_pt = text.rfind(" ", 0, max_w)
        if break_pt == -1: break_pt = max_w
        lines.append(text[:break_pt].strip())
        text = text[break_pt:].strip()
    if text:
        lines.append(text)

    return "\n".join(f"║  {line:<{max_w}}  ║" for line in lines)

def row_empty():
    return f"║{'':^{W}}║"


# ── State parsing ───────────────────────────────────────

def read():
    return STATE.read_text(encoding="utf-8")

def write(content):
    STATE.write_text(content, encoding="utf-8")

def parse_section(content, name):
    m = re.search(rf"## {name}\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    return m.group(1).strip() if m else ""

def parse_active(content):
    raw = parse_section(content, "ACTIVE")
    fields = {}
    for line in raw.splitlines():
        m = re.match(r"^- (\w+): (.+)", line.strip())
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields

def parse_list(content, name):
    raw = parse_section(content, name)
    items = []
    for line in raw.splitlines():
        line = line.strip()
        if line and not line.startswith("_") and not line.startswith(">") and line.lower() != "(empty)":
            m = re.match(r"^[\d]+\.\s+(.+)|^-\s+(.+)", line)
            if m:
                items.append((m.group(1) or m.group(2)).strip())
            else:
                # Fallback cho dòng không có marker nhưng vẫn có data
                items.append(line)
    return items


# ── Dashboard ───────────────────────────────────────────

def show():
    content = read()
    active   = parse_active(content)
    pipeline = parse_list(content, "PIPELINE")
    upcoming = parse_list(content, "UPCOMING")
    # done     = parse_list(content, "DONE") # Bỏ qua DONE

    print(top())
    print(f"║{'CONDUCTOR BOARD':^{W}}║")
    print(mid())

    # ACTIVE
    if active.get("track"):
        agent   = active.get("agent", "?")
        track   = active.get("track", "?")
        phase   = active.get("phase", "?")
        notes   = active.get("notes", "")
        started = active.get("started", "")
        icon  = PHASE_ICON.get(phase.lower(), "⚙")
        label = PHASE_LABEL.get(phase.lower(), phase)
        print(row(f"⚙  ACTIVE  —  {agent}"))
        print(row(f"   {icon} {track}  [{label}]" + (f"  since {started}" if started and started != "—" else "")))
        if notes and notes != "—":
            print(row(f"   💬 {notes}"))
    else:
        print(row("⚙  ACTIVE: (trống — không có track đang chạy)"))

    print(mid())

    # PIPELINE
    print(row("📋 PIPELINE  (sẵn sàng implement)"))
    if pipeline:
        for i, item in enumerate(pipeline[:10], 1):
            print(row(f"   {i}. {item}"))
    else:
        print(row("   (empty)"))

    # UPCOMING
    if upcoming:
        print(row_empty())
        print(row("🔜 UPCOMING  (cần plan)"))
        for i, item in enumerate(upcoming[:10], 1):
            print(row(f"   {i}. {item}"))

    print(bot())
    print(f"\n  state: conductor/state.md")


# ── Commands ─────────────────────────────────────────────

def cmd_done():
    """Move ACTIVE → DONE, promote PIPELINE[0] → ACTIVE"""
    content  = read()
    active   = parse_active(content)
    pipeline = parse_list(content, "PIPELINE")

    if not active.get("track"):
        print("❌  Không có track nào đang ACTIVE.")
        return

    track = active.get("track")
    today = date.today().isoformat()

    # Add to DONE
    done_entry = f"- {track} | {today} | {active.get('agent', '?')}"
    content = re.sub(
        r"(## DONE.*?\n)",
        r"\1" + done_entry + "\n",
        content, count=1, flags=re.DOTALL
    )

    # Clear / promote ACTIVE
    if pipeline:
        next_track = pipeline[0]
        new_active = (
            f"## ACTIVE\n"
            f"- track: {next_track}\n"
            f"- agent: ?\n"
            f"- phase: Dev\n"
            f"- started: {today}\n"
            f"- notes: —\n"
        )
        # Remove first item from PIPELINE (numbered or bulleted)
        content = re.sub(
            r"(## PIPELINE\n(?:>.*\n)*\s*)(?:[\d]+\. |- )(.+)\n",
            r"\1",
            content, count=1
        )
        print(f"✅  {track} → DONE")
        print(f"▶   Promoted: {next_track} → ACTIVE")
    else:
        new_active = (
            f"## ACTIVE\n"
            f"- track: (none)\n"
            f"- agent: —\n"
            f"- phase: —\n"
            f"- started: —\n"
            f"- notes: —\n"
        )
        print(f"✅  {track} → DONE")
        print("ℹ   Pipeline trống — không có track tiếp theo.")

    content = re.sub(
        r"## ACTIVE\n.*?(?=\n## )",
        new_active,
        content, count=1, flags=re.DOTALL
    )
    content = re.sub(r"> Updated: .+", f"> Updated: {today} | Agent: ?", content)
    write(content)


def cmd_note(note):
    content = read()
    updated = re.sub(r"(- notes: ).*", f"\\1{note}", content, count=1)
    updated = re.sub(r"> Updated: .+", f"> Updated: {date.today().isoformat()} | Agent: ?", updated)
    write(updated)
    print(f"📝  Notes updated: {note}")


def cmd_add(name):
    content = read()
    entry   = f"- {name}"
    updated = re.sub(r"(## BACKLOG\n)", f"\\1{entry}\n", content, count=1)
    write(updated)
    print(f"➕  Added to BACKLOG: {name}")


# ── Transition helpers ────────────────────────────────────

def _read_tracks_row(track_id):
    """Return (old_status_str, full_content, regex_pattern) or (None, ...) if not found."""
    content = TRACKS.read_text(encoding="utf-8")
    # Improved pattern to be more flexible with spaces
    pattern = rf"(\| {re.escape(track_id)} \|[^|]+\|)\s*([^|]+?)\s*(\|)"
    m = re.search(pattern, content, re.MULTILINE)
    old_status = m.group(2).strip() if m else None
    return old_status, content, pattern


def _write_tracks_row(content, pattern, new_label):
    new_content = re.sub(
        pattern,
        rf"\g<1> {new_label} \g<3>",
        content, count=1, flags=re.MULTILINE,
    )
    TRACKS.write_text(new_content, encoding="utf-8")


def _update_state_phase(track_id, phase, agent, note=""):
    """Update phase, agent, and notes in state.md if ACTIVE track contains track_id."""
    content      = read()
    active       = parse_active(content)
    active_track = active.get("track", "")
    if track_id.lower() not in active_track.lower():
        return False
    today   = date.today().isoformat()
    content = re.sub(r"(- phase: ).*", f"\\1{phase.capitalize()}", content, count=1)
    if agent and agent != "?":
        content = re.sub(r"(- agent: ).*", f"\\1{agent}", content, count=1)
    if note:
        content = re.sub(r"(- notes: ).*", f"\\1{note}", content, count=1)
    content = re.sub(r"> Updated: .+", f"> Updated: {today} | Agent: {agent}", content)
    write(content)
    return True


def _remove_from_state_lists(content, track_id):
    """Remove any line mentioning track_id from PIPELINE and UPCOMING sections."""
    track_lower = track_id.lower()
    lines = content.split('\n')
    new_lines = []
    in_target_section = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('## '):
            in_target_section = stripped[3:].strip() in ('PIPELINE', 'UPCOMING')

        if in_target_section and stripped and re.match(r'^[\d]+\.\s+|^-\s+', stripped):
            if track_lower in stripped.lower():
                continue  # drop this line
        new_lines.append(line)

    return '\n'.join(new_lines)


def _add_to_state_done(content, track_id, agent):
    """Prepend track entry into DONE section of state.md."""
    today = date.today().isoformat()
    entry = f"- {track_id} | {today} | {agent}"
    # De-duplicate existing DONE rows for this track before prepend
    content = re.sub(
        rf"(?m)^- {re.escape(track_id)}\s*\|.*\n?",
        "",
        content,
    )
    return re.sub(
        r"(## DONE[^\n]*\n)",
        r"\1" + entry + "\n",
        content, count=1,
    )


def _finalize_active_after_done(content, track_id):
    """
    If ACTIVE track is the one being marked done:
    - promote first PIPELINE item to ACTIVE (phase=Dev), or
    - clear ACTIVE to (none) when PIPELINE is empty.
    Returns (new_content, changed_active: bool)
    """
    active = parse_active(content)
    active_track = active.get("track", "")
    if track_id.lower() not in active_track.lower():
        return content, False

    today = date.today().isoformat()
    pipeline = parse_list(content, "PIPELINE")

    if pipeline:
        next_item = pipeline[0]
        next_track = next_item.split("|")[0].strip()
        new_active = (
            f"## ACTIVE\n"
            f"- track: {next_track}\n"
            f"- agent: ?\n"
            f"- phase: Dev\n"
            f"- started: {today}\n"
            f"- notes: —\n"
        )
        # Remove first pipeline row because it is promoted to ACTIVE
        content = re.sub(
            r"(## PIPELINE\n(?:>.*\n)*\s*)(?:[\d]+\.\s+|-\s+).+\n",
            r"\1",
            content,
            count=1,
        )
    else:
        new_active = (
            f"## ACTIVE\n"
            f"- track: (none)\n"
            f"- agent: —\n"
            f"- phase: —\n"
            f"- started: —\n"
            f"- notes: —\n"
        )

    content = re.sub(
        r"## ACTIVE\n.*?(?=\n## )",
        new_active,
        content,
        count=1,
        flags=re.DOTALL,
    )
    return content, True


def _clean_state_lists(track_id, phase, agent):
    """When phase=done: remove from PIPELINE/UPCOMING, finalize ACTIVE, add to DONE."""
    if phase != "done":
        return False
    content = read()
    content = _remove_from_state_lists(content, track_id)
    content, _ = _finalize_active_after_done(content, track_id)
    content = _add_to_state_done(content, track_id, agent)
    today = date.today().isoformat()
    content = re.sub(r"> Updated: .+", f"> Updated: {today} | Agent: {agent}", content)
    write(content)
    return True


def _move_to_pipeline(track_id, agent, note=""):
    """When phase=planned: remove from UPCOMING, add to PIPELINE in state.md."""
    content = read()
    track_lower = track_id.lower()

    # Preserve description from UPCOMING line if present
    found_desc = None
    in_upcoming = False
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('## '):
            in_upcoming = stripped[3:].strip() == 'UPCOMING'
        if in_upcoming and re.match(r'^[\d]+\.\s+|^-\s+', stripped):
            if track_lower in stripped.lower():
                found_desc = re.sub(r'^[\d]+\.\s+|-\s+', '', stripped).strip()
                break

    # Remove from UPCOMING (and PIPELINE if already there)
    content = _remove_from_state_lists(content, track_id)

    # Build entry: use note if provided, else preserve existing desc, else bare id
    if note:
        entry = f"- {track_id} | {note}"
    elif found_desc:
        entry = f"- {found_desc}"
    else:
        entry = f"- {track_id}"

    # Insert after PIPELINE header/comment lines
    content = re.sub(
        r"(## PIPELINE[^\n]*\n(?:>[^\n]*\n)*)",
        lambda m: m.group(0) + entry + "\n",
        content, count=1,
    )
    today = date.today().isoformat()
    content = re.sub(r"> Updated: .+", f"> Updated: {today} | Agent: {agent}", content)
    write(content)
    return True


def _set_active(track_id, phase, agent, note=""):
    """When phase=dev: remove from PIPELINE, set as ACTIVE in state.md."""
    content = read()
    active = parse_active(content)
    current = active.get("track", "(none)")
    today = date.today().isoformat()

    if current not in ("(none)", "", track_id) and track_id.lower() not in current.lower():
        print(f"⚠   ACTIVE hiện tại: '{current}' — sẽ bị override bởi '{track_id}'")

    # Remove from PIPELINE/UPCOMING
    content = _remove_from_state_lists(content, track_id)

    new_active = (
        f"## ACTIVE\n"
        f"- track: {track_id}\n"
        f"- agent: {agent}\n"
        f"- phase: {phase.capitalize()}\n"
        f"- started: {today}\n"
        f"- notes: {note or '—'}\n"
    )
    content = re.sub(
        r"## ACTIVE\n.*?(?=\n## )",
        new_active,
        content, count=1, flags=re.DOTALL,
    )
    content = re.sub(r"> Updated: .+", f"> Updated: {today} | Agent: {agent}", content)
    write(content)
    return True


def _sync_state_for_phase(track_id, phase, agent, note):
    """Auto-sync state.md lists: planned→PIPELINE, dev→ACTIVE."""
    if phase == "planned":
        return _move_to_pipeline(track_id, agent, note)
    if phase == "dev":
        return _set_active(track_id, phase, agent, note)
    return False


def _warn_qa_gate(track_id, phase):
    """For phase=qa: warn if no qa/ folder with artifacts exists in track dir."""
    if phase != "qa":
        return False
    if not TRACKS_DIR.exists():
        return False
    matches = [d for d in TRACKS_DIR.iterdir()
               if d.is_dir() and d.name.lower().startswith(track_id.lower())]
    if not matches:
        return False
    qa_dir = matches[0] / "qa"
    if not qa_dir.exists():
        print(f"⚠   QA GATE: conductor/tracks/{matches[0].name}/qa/ chưa tồn tại")
        print(f"    Cần có artifact test (script + log output) trong qa/ trước khi QA phase")
        return True
    return False


def _update_active_context(track_id, phase):
    """Sync status in docs/memory/00_active_context.md."""
    if not CONTEXT.exists():
        return False

    content = CONTEXT.read_text(encoding="utf-8")
    # Label mapping for context
    label = PHASE_MAP[phase]

    # Pattern to find: - **Track <id>**: ... — **[...]**
    # Supports both **[Label]** and **Label**
    pattern = rf"(- \*\*Track {re.escape(track_id)}\*\*: .*? — \*\*)\[?.*?\]?(\*\*)"

    if re.search(pattern, content):
        new_content = re.sub(pattern, rf"\g<1>{label}\g<2>", content)
        # Also handle special case where it might be "Done" instead of "Completed"
        if phase == "done":
            new_content = new_content.replace(f"**Track {track_id}**: Done", f"**Track {track_id}**: ✅ Completed")

        CONTEXT.write_text(new_content, encoding="utf-8")
        return True
    return False


def _append_changelog(track_id, old_status, new_label, agent, note):
    """Append a row to conductor/tracks/<track-id>*/CHANGELOG.md."""
    if not TRACKS_DIR.exists():
        return False
    matches = [
        d for d in TRACKS_DIR.iterdir()
        if d.is_dir() and d.name.lower().startswith(track_id.lower())
    ]
    if not matches:
        return False
    folder    = matches[0]
    changelog = folder / "CHANGELOG.md"
    today     = date.today().isoformat()
    entry     = f"| {today} | {old_status} | {new_label} | {agent} | {note or '—'} |\n"
    if changelog.exists():
        existing = changelog.read_text(encoding="utf-8")
        changelog.write_text(existing + entry, encoding="utf-8")
    else:
        header = "| Date | From | To | Agent | Note |\n|------|------|----|-------|------|\n"
        changelog.write_text(header + entry, encoding="utf-8")
    return True


def cmd_transition(track_id, phase, agent="?", note=""):
    """
    Atomic status update across 4 files:
      1. conductor/tracks.md        — badge in master list
      2. conductor/state.md         — phase of ACTIVE track (if matches)
      3. conductor/tracks/<id>*/CHANGELOG.md — history entry
      4. docs/memory/00_active_context.md — sync project memory
    """
    if phase not in PHASE_MAP:
        print(f"❌  Phase không hợp lệ: '{phase}'")
        print(f"    Chọn: {', '.join(PHASE_MAP.keys())}")
        return

    new_label = PHASE_MAP[phase]

    # 1. tracks.md
    old_status, tracks_content, pattern = _read_tracks_row(track_id)
    if old_status is None:
        print(f"❌  Track '{track_id}' không tìm thấy trong tracks.md")
        return
    _write_tracks_row(tracks_content, pattern, new_label)

    # 2. state.md (only if ACTIVE matches)
    state_updated = _update_state_phase(track_id, phase, agent, note)

    # 2b. state.md lists: auto-sync per phase
    lists_cleaned = _clean_state_lists(track_id, phase, agent)      # done only
    lists_synced  = _sync_state_for_phase(track_id, phase, agent, note)  # planned / dev

    # 2c. QA gate warn
    _warn_qa_gate(track_id, phase)

    # 3. CHANGELOG.md
    changelog_ok = _append_changelog(track_id, old_status, new_label, agent, note)

    # 4. active_context.md
    context_updated = _update_active_context(track_id, phase)

    print(f"✅  {track_id}:  {old_status}  →  {new_label}")
    print(f"    agent={agent}  note={note or '—'}")
    if state_updated:
        print(f"📋  state.md: phase → {phase}")
    if lists_cleaned:
        print(f"📋  state.md: PIPELINE/UPCOMING → DONE")
    if lists_synced:
        if phase == "planned":
            print(f"📋  state.md: UPCOMING → PIPELINE")
        elif phase == "dev":
            print(f"📋  state.md: PIPELINE → ACTIVE")
    if context_updated:
        print(f"🧠  00_active_context.md: synced")
    if changelog_ok:
        print(f"📝  CHANGELOG.md appended")
    else:
        print(f"⚠   CHANGELOG.md: không tìm thấy conductor/tracks/{track_id}*/")


def cmd_close(track_id, agent="?", note=""):
    """Shortcut for transition <track_id> done [agent] [note]."""
    cmd_transition(track_id, "done", agent, note)


# ── Main ─────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        show()
    elif args[0] in ("done", "next"):
        cmd_done()
    elif args[0] == "note" and len(args) >= 2:
        cmd_note(" ".join(args[1:]))
    elif args[0] == "add" and len(args) >= 2:
        cmd_add(" ".join(args[1:]))
    elif args[0] == "close" and len(args) >= 2:
        track_id = args[1]
        agent    = args[2] if len(args) > 2 else "?"
        note     = " ".join(args[3:]) if len(args) > 3 else ""
        cmd_close(track_id, agent, note)
    elif args[0] == "transition" and len(args) >= 3:
        track_id = args[1]
        phase    = args[2]
        agent    = args[3] if len(args) > 3 else "?"
        note     = " ".join(args[4:]) if len(args) > 4 else ""
        cmd_transition(track_id, phase, agent, note)
    else:
        print(__doc__)
