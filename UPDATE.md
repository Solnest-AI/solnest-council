# UPDATE — Solnest Council (Claude reads this)

**You are Claude. The user pasted this repo's link and asked you to update their Solnest Council. Do it FOR them, in plain language. Never paste a raw error at them.**

---

## Step 0 — Find their install

The Council lives in **two places**. Check both:

- Skill: `~/.claude/skills/solnest-council/` (Windows: `%USERPROFILE%\.claude\skills\solnest-council\`)
- Agents: `~/.claude/agents/council-*.md` (Windows: `%USERPROFILE%\.claude\agents\`)

If the skill folder isn't there, they never installed it. Tell them to grab the zip from the Skool community and drag it in for a fresh install, and stop here.

If the skill is there but the **agents are missing or fewer than 18**, that's a broken install, not an update. Say so plainly, then fix it by doing Step 4 below — that alone will repair them.

## Step 1 — Check if they even need this

Compare `VERSION` in their install to `VERSION` in this repo. If they match **and** they have all 18 agents, say so and stop:

> You're already on the latest version (`X.Y.Z`) with all 18 members. Nothing to update.

## Step 2 — What to preserve

**Their custom council members, if they made any.**

The 18 that ship with this skill are all named `council-<figure>.md`. If they've added agents of their own to `~/.claude/agents/` — including any *extra* council members they wrote themselves — **those are theirs and must survive.**

So: **only overwrite the 18 filenames this package ships.** Never wipe `~/.claude/agents/` and never delete an agent file that isn't one of ours. Get the list of ours from the `agents/` folder in the fresh clone — don't work from memory.

Also preserve **`configs/`** if they've edited it. Before overwriting, check whether their `configs/auto-route-defaults.yaml` differs from the repo's. If it does, they've tuned their model routing — **back it up first**, copy the new one in, then tell them their old config is saved alongside it and let them decide. Don't silently overwrite a config they tuned.

## Step 3 — Pull the latest

```bash
git clone --depth 1 https://github.com/Solnest-AI/solnest-council.git /tmp/solnest-council-update
```

No `git`? Download `https://github.com/Solnest-AI/solnest-council/archive/refs/heads/main.zip` instead.

## Step 4 — Copy the new files over — BOTH halves

**Half 1 — the skill:**
```bash
cp -R /tmp/solnest-council-update/. ~/.claude/skills/solnest-council/
chmod +x ~/.claude/skills/solnest-council/scripts/detect-providers.sh
```
File over file. Don't delete the folder first.

**Half 2 — the agents (the step people forget):**
```bash
cp /tmp/solnest-council-update/agents/council-*.md ~/.claude/agents/
```
This overwrites only the 18 council files and leaves every other agent they own alone.

## Step 5 — Verify both halves

```bash
test -f ~/.claude/skills/solnest-council/SKILL.md && echo "skill: OK"
echo "agents: $(ls ~/.claude/agents/council-*.md 2>/dev/null | wc -l | tr -d ' ') of 18"
cat ~/.claude/skills/solnest-council/VERSION
```

You must see **18 of 18** and the new version number. If not, fix it before telling them you're done.

## Step 6 — Restart

They must **fully quit and reopen Claude Code** — not just the window — or the updated agents won't be picked up.

## Step 7 — Tell them what changed

Read `CHANGELOG.md` from the fresh copy and give them two or three plain-English bullets for the **new version only** — not the whole file. Then:

> Updated to `X.Y.Z`, all 18 members refreshed. Quit and reopen Claude Code and you're good.

## If something goes wrong

Tell them in one friendly sentence. Nothing here is destructive — the Council stores no data of theirs, and they can always reinstall from the Skool zip.
