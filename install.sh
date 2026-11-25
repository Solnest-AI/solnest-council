#!/usr/bin/env bash
# Solnest Council installer (macOS, Linux, and Windows through Git Bash). No admin rights,
# no PATH edits, nothing to type afterwards. Re-run any time to repair: it keeps every
# file you added, your routing settings if you changed them, and any council member you
# edited.
#
# Run it from Claude Code's Bash tool, or any terminal:
#   bash -o pipefail -c "curl -fsSL https://raw.githubusercontent.com/Solnest-AI/solnest-council/main/install.sh | bash"
# or, from a copy of the repo:  bash install.sh
#
# What it does: copies the skill into ~/.claude/skills/solnest-council, finds a Python 3.9+
# (or installs one through uv, no admin needed) for the updater, writes a launcher (bin/py),
# copies the 18 council members into ~/.claude/agents, and proves all 18 are there and the
# updater starts.
set -u

REPO="Solnest-AI/solnest-council"
BRANCH="${COUNCIL_BRANCH:-main}"             # override to test a branch
ARCHIVE="${COUNCIL_ARCHIVE_URL:-https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz}"   # override for offline tests
NAME="solnest-council"
DEST="$HOME/.claude/skills/$NAME"
SETTINGS="configs/auto-route-defaults.yaml"   # the member's routing settings
HERE=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

OS="$(uname -s)"
WIN=0
case "$OS" in MINGW*|MSYS*|CYGWIN*) WIN=1 ;; esac

echo "Solnest Council installer ($OS)"

# 0. Never overwrite something that is not ours.
if [ -L "$DEST" ]; then
  echo "STOP: $DEST is a link to a folder somewhere else. Nothing was changed."
  exit 3
fi
if [ -e "$DEST/.git" ]; then
  echo "STOP: $DEST is a git checkout (a developer's copy). Nothing was changed."
  exit 3
fi
if [ -f "$DEST/SKILL.md" ] && ! grep -q '^name: solnest-council[[:space:]]*$' "$DEST/SKILL.md"; then
  echo "STOP: $DEST holds a different skill. Nothing was changed. Move it away, then run this again."
  exit 3
fi

# 1. The skill files: this copy of the repo if we are running from one, else a download.
SRC=""
TMP=""
if [ -n "$HERE" ] && [ "$HERE" != "$DEST" ] && [ -f "$HERE/SKILL.md" ] && [ -d "$HERE/agents" ]; then
  SRC="$HERE"
else
  TMP="$(mktemp -d 2>/dev/null || mktemp -d -t solnest-council)"
  echo "  downloading the skill..."
  if ! curl -fsSL --retry 3 "$ARCHIVE" -o "$TMP/repo.tar.gz"; then
    echo "ERROR: could not download the skill from GitHub. Check the internet connection and run this again."
    exit 2
  fi
  if ! tar -xzf "$TMP/repo.tar.gz" -C "$TMP"; then
    echo "ERROR: the download could not be unpacked. Run this again."
    exit 2
  fi
  SRC="$(ls -d "$TMP"/*/agents 2>/dev/null | head -1)"
  SRC="${SRC%/agents}"
  if [ -z "$SRC" ] || [ ! -f "$SRC/SKILL.md" ]; then
    echo "ERROR: the download did not contain the skill."
    exit 2
  fi
fi

# A copy installed before the council kept a record of its members: remember what that copy
# shipped, so a member you changed since can be told apart from one that is just older.
BASE=""
if [ -d "$DEST/agents" ] && [ ! -f "$DEST/.council-agents.json" ]; then
  rm -rf "$DEST/.agents-before"
  mkdir -p "$DEST/.agents-before" && cp "$DEST"/agents/council-*.md "$DEST/.agents-before/" 2>/dev/null && BASE="$DEST/.agents-before"
fi

# Copy the skill's own files over. Files you added to the folder are left alone, and so are
# your routing settings once they exist. The repo's housekeeping (tests, .github), a stray
# .cursor folder and Python caches are never installed.
mkdir -p "$DEST"
( cd "$SRC" && find . -type f ! -path './.git/*' ! -path '*/.cursor/*' ! -path '*/__pycache__/*' \
    ! -path './tests/*' ! -path './.github/*' ! -path './bin/*' ! -path './.update-backup/*' \
    ! -path './.agents-before/*' ! -path './.pytest_cache/*' ! -name '.DS_Store' ! -name '.gitignore' \
    ! -name '.gitattributes' ! -name '.env' ! -name '.env.*' ! -name '.council-*' ! -name '*.update-tmp' \
    ! -path './configs/provider-model-slots.yaml' ) | while IFS= read -r f; do
  f="${f#./}"
  if [ "$f" = "$SETTINGS" ] && [ -f "$DEST/$f" ] && ! cmp -s "$SRC/$f" "$DEST/$f"; then
    echo "[ok] settings  kept your own $SETTINGS"
    continue
  fi
  mkdir -p "$DEST/$(dirname "$f")"
  cp "$SRC/$f" "$DEST/$f"
done
chmod +x "$DEST/scripts/detect-providers.sh" 2>/dev/null
# The old install guide from before 1.2.0 (ours, now replaced by CLAUDE.md): take it away.
if [ -f "$DEST/START-HERE.md" ] && grep -q 'Auto-installer (Claude reads this)' "$DEST/START-HERE.md"; then
  rm -f "$DEST/START-HERE.md"
fi
echo "[ok] skill     $DEST"

# 2. A Python that works here (3.9 or newer). On a Mac without the Xcode command line
#    tools, /usr/bin/python3 is a stub that pops up a dialog, so it is skipped. On Windows
#    the Microsoft Store alias (WindowsApps) is tried last: on a fresh machine it is a stub.
python_ok() { "$@" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; }
real_path() { "$@" -c 'import sys; print(sys.executable)' 2>/dev/null | tr -d '\r' | tr '\\' '/'; }
PY=""
LATER=""
for c in python3 python; do
  p="$(command -v "$c" 2>/dev/null)" || continue
  if [ "$OS" = "Darwin" ] && { [ "$p" = "/usr/bin/python3" ] || [ "$p" = "/usr/bin/python" ]; }; then
    xcode-select -p >/dev/null 2>&1 || continue
  fi
  case "$p" in *WindowsApps*) LATER="$LATER $c"; continue ;; esac
  python_ok "$p" && { PY="$(real_path "$p")"; break; }
done
if [ -z "$PY" ] && command -v py >/dev/null 2>&1 && python_ok py -3; then
  PY="$(real_path py -3)"
fi
find_uv_python() {
  for u in uv "$HOME/.local/bin/uv" "$HOME/.local/bin/uv.exe"; do
    command -v "$u" >/dev/null 2>&1 || continue
    p="$("$u" python find 3.13 2>/dev/null | tr -d '\r' | tr '\\' '/')"
    [ -n "$p" ] && python_ok "$p" && { PY="$p"; return 0; }
    "$u" python install 3.13 >/dev/null 2>&1
    p="$("$u" python find 3.13 2>/dev/null | tr -d '\r' | tr '\\' '/')"
    [ -n "$p" ] && python_ok "$p" && { PY="$p"; return 0; }
  done
  return 1
}
if [ "$WIN" = 1 ] && [ -z "${UV_PYTHON_INSTALL_DIR:-}" ]; then
  # The Claude desktop app on Windows redirects AppData writes; keep uv's Python under the profile.
  export UV_PYTHON_INSTALL_DIR="$(cygpath -w "$HOME/.uv/python" 2>/dev/null || echo "$HOME/.uv/python")"
fi
[ -z "$PY" ] && find_uv_python
if [ -z "$PY" ]; then
  for c in $LATER; do
    p="$(command -v "$c" 2>/dev/null)" || continue
    python_ok "$p" && { PY="$(echo "$p" | tr '\\' '/')"; break; }
  done
fi
if [ -z "$PY" ]; then
  echo "  installing Python (through uv, no admin needed)..."
  if [ "$WIN" = 1 ]; then
    powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex" >/dev/null 2>&1
  else
    curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
  fi
  find_uv_python
fi
if [ -z "$PY" ]; then
  echo "ERROR: no working Python 3.9+ was found and the automatic install failed."
  echo "       Install Python from https://www.python.org/downloads/ (Windows: tick 'Add python.exe to PATH'), then run this again."
  [ -n "$TMP" ] && rm -rf "$TMP"
  exit 2
fi
echo "[ok] Python    $PY"

# 3. The launcher: every command in the skill runs through bin/py, so it never depends on PATH.
mkdir -p "$DEST/bin"
cat > "$DEST/bin/py" <<EOF
#!/bin/sh
# Python launcher for the Solnest Council skill, written by install.sh.
# Runs the Python found at install time; falls back to whatever works if it moved.
P="$PY"
if [ -x "\$P" ]; then exec "\$P" "\$@"; fi
for c in python3 python; do
  q="\$(command -v "\$c" 2>/dev/null)" || continue
  case "\$q" in
    *WindowsApps*) continue ;;
    /usr/bin/python3) xcode-select -p >/dev/null 2>&1 || continue ;;
  esac
  "\$q" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1 && exec "\$q" "\$@"
done
if command -v py >/dev/null 2>&1; then exec py -3 "\$@"; fi
echo "ERROR: no Python found. Run the Solnest Council installer again." >&2
exit 1
EOF
chmod +x "$DEST/bin/py"
if [ "$WIN" = 1 ]; then
  WPY="$(cygpath -w "$PY" 2>/dev/null || echo "$PY")"
  printf '@echo off\r\nrem Python launcher for the Solnest Council skill (PowerShell / cmd), written by install.sh.\r\n"%s" %%*\r\nexit /b %%errorlevel%%\r\n' "$WPY" > "$DEST/bin/py.cmd"
fi
echo "[ok] launcher  $DEST/bin/py"

# 4. The 18 council members go into ~/.claude/agents (Claude Code only finds agents there).
rc=0
if [ -n "$BASE" ]; then
  "$DEST/bin/py" "$DEST/scripts/install_agents.py" --baseline "$BASE" || rc=1
  rm -rf "$BASE"
else
  "$DEST/bin/py" "$DEST/scripts/install_agents.py" || rc=1
fi

# 5. Prove the updater starts.
if "$DEST/bin/py" "$DEST/scripts/update.py" --help >/dev/null 2>&1; then
  echo "[ok] updater   starts"
else
  echo "[!!] updater   did not start. Run this installer again."
  rc=1
fi
echo "[ok] version   $(tr -d '[:space:]' < "$DEST/VERSION" 2>/dev/null || echo unknown)"

[ -n "$TMP" ] && rm -rf "$TMP"
exit $rc
