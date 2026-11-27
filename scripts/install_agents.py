#!/usr/bin/env python3
"""Put the council members where Claude Code looks for agents, and prove they are all there.

    <python> scripts/install_agents.py                  copy the members, then count them
    <python> scripts/install_agents.py --check          only count them, change nothing
    <python> scripts/install_agents.py --baseline DIR   DIR holds the members an older copy shipped

The skill folder keeps the members in agents/council-*.md. Claude Code only finds agents in
~/.claude/agents, so every install and every update copies them there. The installer runs
this, and so does the auto-updater after each new release (its "after" step). Exit code 0
means every member this release ships is in place; anything else means the panel is not
whole, and the auto-updater then puts the previous release back.

What it never does:
- touch an agent file that is not one of the members this skill ships;
- overwrite a member the user changed. .council-agents.json (in the skill folder) records
  what was last put there, so a file that no longer matches is the user's own and stays.
  To get the standard member back, delete that file and run this again.
- lose a file when there is no record to go by (a copy installed before this script
  existed): a member that differs is saved to ~/.solnest/council/agents-saved/ first.

Standard library only. SOLNEST_COUNCIL_AGENTS_DIR points it at another agents folder (tests).
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SHIPPED = SKILL / "agents"
RECORD = SKILL / ".council-agents.json"
PATTERN = "council-*.md"


def live_dir() -> Path:
    return Path(os.environ.get("SOLNEST_COUNCIL_AGENTS_DIR") or (Path.home() / ".claude" / "agents")).expanduser()


def saved_dir() -> Path:
    home = Path(os.environ.get("SOLNEST_HOME") or (Path.home() / ".solnest")).expanduser()
    return home / "council" / "agents-saved"


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".update-tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def _load_record() -> dict[str, str]:
    try:
        data = json.loads(RECORD.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {k: v for k, v in data.items() if isinstance(k, str) and isinstance(v, str)} if isinstance(data, dict) else {}


def sync(baseline: Path | None = None) -> dict:
    """Copy every shipped member into the live agents folder. Returns what happened."""
    live = live_dir()
    record = _load_record()
    had_record = RECORD.is_file()
    new_record: dict[str, str] = {}
    out = {"installed": [], "same": [], "kept": [], "saved": [], "removed": []}
    shipped = sorted(SHIPPED.glob(PATTERN))
    for src in shipped:
        name, data = src.name, src.read_bytes()
        want = _hash(data)
        dest = live / name
        if not dest.is_file():
            _write(dest, data)
            out["installed"].append(name)
        else:
            have_bytes = dest.read_bytes()
            have = _hash(have_bytes)
            base = baseline / name if baseline else None
            ours = have == record.get(name) or bool(base and base.is_file() and _hash(base.read_bytes()) == have)
            if have == want:
                out["same"].append(name)
            elif ours:
                _write(dest, data)
                out["installed"].append(name)
            elif had_record or (base and base.is_file()):
                out["kept"].append(name)            # the user changed this member: it stays theirs
            else:
                stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                _write(saved_dir() / f"{name}.{stamp}", have_bytes)
                _write(dest, data)
                out["saved"].append(name)
        new_record[name] = want
    # A member an older release shipped and this one does not: remove it, unless the user changed it.
    for name, old in record.items():
        dest = live / name
        if name not in new_record and dest.is_file() and _hash(dest.read_bytes()) == old:
            dest.unlink()
            out["removed"].append(name)
    if shipped:
        _write(RECORD, (json.dumps(new_record, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    return out


def check() -> tuple[int, int]:
    """(members in the live folder, members this release ships)."""
    live = live_dir()
    names = [p.name for p in SHIPPED.glob(PATTERN)]
    return sum(1 for n in names if (live / n).is_file()), len(names)


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        with contextlib.suppress(AttributeError, ValueError):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Install the council members into the Claude Code agents folder.")
    ap.add_argument("--check", action="store_true", help="only count them, change nothing")
    ap.add_argument("--baseline", help="folder of the members an older copy shipped")
    args = ap.parse_args()
    try:
        if not args.check:
            r = sync(Path(args.baseline) if args.baseline else None)
            if r["kept"]:
                print(f"[agents] Kept your own version of: {', '.join(r['kept'])}")
            if r["saved"]:
                print(f"[agents] Replaced {len(r['saved'])} member(s) that differed; the old copies are in {saved_dir()}")
        have, want = check()
    except OSError as e:
        print(f"[agents] could not install the council members ({type(e).__name__}: {e})", file=sys.stderr)
        return 1
    ok = want > 0 and have == want
    print(f"[{'ok' if ok else '!!'}] agents    {have} of {want} in {live_dir()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
