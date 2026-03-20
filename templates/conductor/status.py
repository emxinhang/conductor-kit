#!/usr/bin/env python3
"""
conductor/status.py — TMS-2026 Conductor Dashboard

Usage:
  python conductor/status.py              # Show dashboard
  python conductor/status.py done         # Mark ACTIVE track as done, promote PIPELINE[0]
  python conductor/status.py next         # Alias for done
  python conductor/status.py note "..."   # Update ACTIVE notes
  python conductor/status.py add "name"   # Add track to BACKLOG
"""

import sys
import re
from pathlib import Path
from datetime import date

STATE = Path(__file__).parents[2] / "conductor" / "state.md"
W = 56  # box width


# ── Box drawing ────────────────────────────────────────

def top(): return "╔" + "═" * W + "╗"
def mid(): return "╠" + "═" * W + "╣"
def bot(): return "╚" + "═" * W + "╝"

def row(text=""):
    text = str(text)
    if len(text) > W - 4:
        text = text[:W - 7] + "..."
    return f"║  {text:<{W - 4}}  ║"

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
        if line and not line.startswith("_") and not line.startswith(">"):
            # numbered list: "1. foo" or bullet: "- foo"
            m = re.match(r"^[\d]+\.\s+(.+)|^-\s+(.+)", line)
            if m:
                items.append((m.group(1) or m.group(2)).strip())
    return items


# ── Dashboard ───────────────────────────────────────────

def show():
    content = read()
    active = parse_active(content)
    pipeline = parse_list(content, "PIPELINE")
    upcoming = parse_list(content, "UPCOMING")
    done = parse_list(content, "DONE")

    print(top())
    print(f"║{'I-CHING — CONDUCTOR BOARD':^{W}}║")
    print(mid())

    # ACTIVE
    if active.get("track"):
        agent = active.get("agent", "?")
        track = active.get("track", "?")
        phase = active.get("phase", "?")
        notes = active.get("notes", "")
        print(row(f"⚙  {agent} ĐANG LÀM"))
        print(row(f"   {track}  →  {phase}"))
        if notes and notes != "—":
            print(row(f"   {notes}"))
    else:
        print(row("⚙  ACTIVE: (trống — không có track đang chạy)"))

    print(mid())

    # PIPELINE
    print(row("📋 PIPELINE  (sẵn sàng implement)"))
    if pipeline:
        for i, item in enumerate(pipeline[:4], 1):
            print(row(f"   {i}. {item}"))
    else:
        print(row("   (empty)"))

    # UPCOMING
    if upcoming:
        print(row_empty())
        print(row("🔜 UPCOMING  (cần plan)"))
        for i, item in enumerate(upcoming[:3], 1):
            print(row(f"   {i}. {item}"))

    print(mid())

    # DONE
    print(row("✅ DONE GẦN ĐÂY"))
    for item in done[:4]:
        print(row(f"   {item}"))

    print(bot())
    print(f"\n  state: conductor/state.md")


# ── Commands ─────────────────────────────────────────────

def cmd_done():
    """Move ACTIVE → DONE, promote PIPELINE[0] → ACTIVE"""
    content = read()
    active = parse_active(content)
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

    # Clear ACTIVE
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
        # Remove first pipeline item
        content = re.sub(
            r"(## PIPELINE\n.*?\n)1\. .+\n",
            lambda m: m.group(0).replace(
                re.search(r"1\. .+", m.group(0)).group(), "", 1
            ),
            content, count=1, flags=re.DOTALL
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

    # Update ACTIVE section
    content = re.sub(
        r"## ACTIVE\n.*?(?=\n## )",
        new_active,
        content, count=1, flags=re.DOTALL
    )

    # Update timestamp
    content = re.sub(r"> Updated: .+", f"> Updated: {today} | Agent: ?", content)
    write(content)


def cmd_note(note):
    content = read()
    updated = re.sub(
        r"(- notes: ).*",
        f"\\1{note}",
        content, count=1
    )
    updated = re.sub(r"> Updated: .+", f"> Updated: {date.today().isoformat()} | Agent: ?", updated)
    write(updated)
    print(f"📝  Notes updated: {note}")


def cmd_add(name):
    content = read()
    entry = f"- {name}"
    updated = re.sub(
        r"(## BACKLOG\n)",
        f"\\1{entry}\n",
        content, count=1
    )
    write(updated)
    print(f"➕  Added to BACKLOG: {name}")


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
    else:
        print(__doc__)
