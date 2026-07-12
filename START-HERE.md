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

**At this point the Council is fully installed and working.** Everything below is optional.

---

## Step 5 — Offer the multi-model upgrade — AND OFFER TO SKIP IT

**Stop and ask. Do not start installing anything.** The Council is already done and working on Claude alone. This step is a genuine offer, not a formality, and **skipping is a perfectly good answer** — most people should.

Ask them roughly this, and wait:

> The Council works right now, on Claude, and you can go use it.
>
> There's one optional upgrade. Right now all 18 members are Claude — they argue well, but underneath it's one model arguing with itself. If you add a second model, the Council splits the **opposing pairs across different engines** — Socrates on one, Feynman on another. The disagreement becomes real instead of simulated.
>
> Want to set that up now, or skip it? **You can add it any time later — nothing is lost by skipping.**
>
> 1. **Skip for now** — go use the Council. *(Totally fine. Most people start here.)*
> 2. **Ollama** — free, runs on your own machine, no key, no account. *(Easiest, and my pick if you want one.)*
> 3. **Gemini** — free API key from Google.
> 4. **Codex (GPT)** — works with any ChatGPT account, free tier included.
> 5. **NVIDIA NIM** — free credits, one key, no CLI needed.

### If they skip

Say so cheerfully and go straight to Step 6. **Do not talk them into it.** Do mention once, briefly, that `SETUP-MODELS.md` in the skill folder has it whenever they want it — then drop it.

### If they want one

Open **`SETUP-MODELS.md`** in this folder and follow the section for the option they picked. Do it *for* them where you can. **Set up only what they asked for** — one provider is enough to get real cross-model friction. Don't upsell them into all four.

Two things you must get right:

- **🚨 If they choose Gemini, the API key is mandatory — not optional.** The Council detects Gemini by checking the `gemini` command runs; **it never checks whether they're signed in.** So a Gemini CLI installed *without* a `GEMINI_API_KEY` is the one genuinely broken state: the Council will assign council seats to Gemini and **those members will fail mid-deliberation.** Either finish the key, or don't install the CLI. Never leave them half-done. (And never tell them to sign in with a Google account — that path is dead.)
- **These are the CLI tools, not the Claude Code plugins.** If they have Solnest Three-Brain installed, that gave them the `/codex:*` and `/gemini:*` *plugins* — which is a different thing. The Council needs the actual `codex` / `gemini` commands. Don't assume one implies the other; verify.

### Verify it actually worked

Whatever they added, prove it before claiming success:

```bash
bash ~/.claude/skills/solnest-council/scripts/detect-providers.sh
```

Read `provider_count` in the JSON. It must now be **2 or more**. If it still says `1`, the new provider isn't visible to the Council — fix that, or tell them plainly it didn't take and they're on Claude-only (which still works fine). **Don't claim multi-model is live without seeing that number go up.**

---

## Step 6 — Tell them they're done

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

**If they set up a second model in Step 5**, add this — and show them the proof:

> You're running multi-model now, so the opposing thinkers are on different engines. Want to see who's on what? Run:
> `/solnest-council --dry-route --full <any question>`
> That prints the routing table and stops without spending anything.

**If they skipped**, say nothing more about it. It's in `SETUP-MODELS.md` when they want it.
