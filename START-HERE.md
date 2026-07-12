# START HERE — Auto-installer (Claude reads this)

**You are Claude running in Claude Code. The user just dragged in this folder to install the "Solnest Council" skill. Do the install FOR them now, one step at a time, in plain language. Never paste a raw error at them — fix it quietly, or explain it in one friendly sentence.**

This skill is **text-only — nothing to compile, no API keys, no accounts.** It works out of the box with just Claude.

> ⚠️ **This install copies to TWO places, not one.** Most skills are a single folder copy. This one isn't. The skill goes in the skills folder, and **18 council-member agents go in the agents folder.** If you only do the first half, `/solnest-council` will look installed and then fail the moment it tries to convene the panel. Do both halves and verify both.

> ⚠️ **Claude Code, not the Claude Desktop app.** The Council works by spawning subagents, which the desktop app can't do. If the user is in the desktop app, tell them plainly and stop.

---

## Step 1 — Copy the skill

- **Source:** the folder this `START-HERE.md` is sitting in (it contains `SKILL.md`).
- **Destination:** `~/.claude/skills/solnest-council` (Windows: `%USERPROFILE%\.claude\skills\solnest-council`)

The whole folder goes in — `SKILL.md`, `configs/`, and `scripts/`. **The `configs/` and `scripts/` folders are required**, not optional extras: the skill reads them at runtime by absolute path.

**macOS / Linux:**
```bash
mkdir -p ~/.claude/skills
cp -R "<<THIS_FOLDER>>" ~/.claude/skills/solnest-council
chmod +x ~/.claude/skills/solnest-council/scripts/detect-providers.sh
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force "<<THIS_FOLDER>>" "$env:USERPROFILE\.claude\skills\solnest-council"
```

(Replace `<<THIS_FOLDER>>` with the real path of the folder you're reading this from.)

## Step 2 — Copy the 18 council members into the agents folder

This is the half that gets forgotten. The 18 agents live in `agents/` inside this package, but they must be installed into the user's **agents** folder — a different place from the skill.

- **Source:** `agents/council-*.md` inside this package (18 files)
- **Destination:** `~/.claude/agents/` (Windows: `%USERPROFILE%\.claude\agents\`)

They go in **flat, directly into `agents/`** — not in a subfolder. Claude Code only discovers agents at the top level of that directory.

**macOS / Linux:**
```bash
mkdir -p ~/.claude/agents
cp "<<THIS_FOLDER>>"/agents/council-*.md ~/.claude/agents/
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\agents" | Out-Null
Copy-Item -Force "<<THIS_FOLDER>>\agents\council-*.md" "$env:USERPROFILE\.claude\agents\"
```

If any `council-*.md` already exist there, overwrite them — that's just an older copy of the same members.

> The skill folder also keeps its own copy of `agents/`. That's intentional — it's the source for future updates. The *live* agents are the ones in `~/.claude/agents/`.

## Step 3 — Verify BOTH halves landed

Don't skip this. Check and report the actual counts:

**macOS / Linux:**
```bash
test -f ~/.claude/skills/solnest-council/SKILL.md && echo "skill: OK" || echo "skill: MISSING"
test -f ~/.claude/skills/solnest-council/scripts/detect-providers.sh && echo "scripts: OK" || echo "scripts: MISSING"
echo "agents installed: $(ls ~/.claude/agents/council-*.md 2>/dev/null | wc -l | tr -d ' ') of 18"
```

**Windows (PowerShell):**
```powershell
Test-Path "$env:USERPROFILE\.claude\skills\solnest-council\SKILL.md"
(Get-ChildItem "$env:USERPROFILE\.claude\agents\council-*.md").Count
```

**You must see `18 of 18`.** If it's fewer, copy the missing ones before continuing — a partial panel produces a lopsided verdict, which is worse than no panel at all because it looks like it worked.

## Step 4 — Restart

Tell the user to **fully quit and reopen Claude Code** — not just the window. New agents are only discovered at startup.

## Step 5 — Tell them they're done

Say something like:

> You've got a Council. 18 thinkers — Socrates, Feynman, Torvalds, Machiavelli, Taleb, Kahneman, Munger, Rams and more — that you can convene on any hard call, and they're built to **disagree with each other on purpose**.
>
> Try it on a real decision you're stuck on:
> - **`/solnest-council --triad strategy Should I raise my prices?`** — three thinkers, fast.
> - **`/solnest-council --duo Should we ship this now or wait?`** — two opposites argue it out.
> - **`/solnest-council --full <your hardest question>`** — all 18. It's slow, and it's worth it.
>
> Or just say **"convene the council on this"** any time.

Mention one thing they'd otherwise discover the hard way: **`--full` spawns 18 agents and burns real tokens.** Suggest they start with `--triad` or `--quick`. It's not broken, it's just genuinely doing 18 agents' worth of thinking.
