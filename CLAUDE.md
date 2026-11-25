If the user said "set this up", follow SETUP below.

# Solnest Council (Solnest AI)

This repo installs the `solnest-council` skill and its 18 council members. When the user says "convene the council" (or runs `/solnest-council`), the skill has you run a panel of 18 historical thinkers as separate agents, make them question each other, and return one verdict that shows where they agreed and where they did not.

What is in here:
- `SKILL.md`, `configs/`, `scripts/`: the skill. This whole folder installs to `~/.claude/skills/solnest-council`.
- `agents/council-*.md`: the 18 members. They also get copied to `~/.claude/agents`, because that is the only place Claude Code finds agents. A copy in the skill folder alone does nothing.
- `install.sh`: the installer. `VERSION` and `CHANGELOG.md`: what release this is. `SETUP-MODELS.md`: the optional second-model guide.

The Council is built on the open-source `council-of-high-intelligence` project by nyk (MIT license, kept in `LICENSE`). Solnest AI added the setup, the guides and the automatic updates.

## Your own changes (read first, every time)

Before anything else, read `~/.solnest/council/my-instructions.md` if it exists and
follow it. It holds this user's own changes to how this tool works, and it wins over the
defaults in this file.

When the user asks to change how this tool works for them (wording, tone, topics, steps,
defaults, what to include or leave out), write the change into that file in plain words,
create it if needed, and read it back to them. **Never edit this tool's own files for
that.** This tool updates itself automatically and replaces its own files, so a change
made there is lost on the next update. An update never touches that file. It also keeps
their routing settings (`configs/auto-route-defaults.yaml`) if they changed them, their own
seat map (`configs/provider-model-slots.yaml`), any council member they edited in
`~/.claude/agents`, and every agent or file they added themselves.

## Rules for you (Claude) during setup

- You run every command yourself with your Bash tool. The user never opens a terminal. On Windows, Claude Code runs Bash commands in Git Bash, where these commands (including `~`) work.
- One step per message. Do not report success until you have seen real output.
- The Council needs no accounts and no keys. Never ask for one. The optional second model (Step 6) may use a key: it never goes in the chat, see `SETUP-MODELS.md`.
- This must be Claude Code. In the plain Claude chat app there are no agents, so the Council cannot run. If that is where you are, say so in one line and stop.

## SETUP

### Step 1: Look for a copy that is already there

Run:

```bash
D="$HOME/.claude/skills/solnest-council"; if [ -L "$D" ]; then echo "LINK"; elif [ -e "$D/.git" ]; then echo "GIT COPY"; elif [ -f "$D/VERSION" ]; then echo "SOLNEST COPY $(cat "$D/VERSION")"; elif [ -e "$D" ]; then echo "OTHER COPY"; else echo "NOTHING THERE"; fi; echo "members now: $(ls "$HOME"/.claude/agents/council-*.md 2>/dev/null | wc -l | tr -d ' ')"
```

- `NOTHING THERE` or `SOLNEST COPY`: go to Step 2. An older Solnest copy is brought up to date in place and keeps its settings.
- `LINK`, `GIT COPY` or `OTHER COPY`: something else lives in that folder. Tell the user what you found and stop. Do not delete it yourself.

### Step 2: Install

Tell the user in one line: "Installing the Council and its 18 members. About a minute, nothing for you to do." Then run one of these:

- You are reading this from the GitHub page (no local copy of this repo):

  ```bash
  bash -o pipefail -c "curl -fsSL https://raw.githubusercontent.com/Solnest-AI/solnest-council/main/install.sh | bash"
  ```

- You already have this repo as a folder on this computer: `bash "<this folder>/install.sh"`

The installer copies the skill to `~/.claude/skills/solnest-council`, finds Python 3.9 or newer (or installs one for this user, no admin rights needed), writes a small launcher (`bin/py`) so the updater always uses that Python, copies the 18 members into `~/.claude/agents`, and proves the updater starts. Running it again is safe: it leaves alone every file the user added, their routing settings if they changed them, and any member they edited.

### Step 3: Read the checklist it printed

- Every line starts with `[ok]`, and the agents line says `18 of 18`: go on to Step 4.
- `[ok] settings  kept your own ...`: the user had changed their routing settings, so they were kept. Nothing to do.
- `[agents] Kept your own version of: ...`: the user had edited those members, so they were kept. Tell them in one line.
- `[agents] Replaced N member(s) that differed`: an older copy was replaced and the old files were saved in the folder it names. Tell them in one line.
- `[!!] agents    N of 18`: the panel is not whole. Run Step 2 once more. A short panel gives a lopsided verdict, so do not go on until it says 18 of 18.
- `STOP: ...`: something else lives at `~/.claude/skills/solnest-council`. Nothing was changed. Go back to Step 1.
- `ERROR: could not download`: usually the network. Run Step 2 once more.
- `ERROR: no working Python`: send the user to https://www.python.org/downloads/ (on Windows they must tick "Add python.exe to PATH"). When they say it is installed, run Step 2 again.
- `[!!] updater`: run Step 2 once more. If it repeats, send the full output to hello@solnestai.com.

### Step 4: Real test (read-only)

Run:

```bash
S="$HOME/.claude/skills/solnest-council"; "$S/bin/py" "$S/scripts/install_agents.py" --check && grep -c '^name: solnest-council' "$S/SKILL.md" && bash "$S/scripts/detect-providers.sh"
```

Expect three things: `[ok] agents    18 of 18`, then `1`, then one line of JSON. In the JSON read `provider_count`: `1` means the Council runs on Claude alone (normal), `2` or more means other models were found and opposing members will be split across them. This check changes nothing and costs nothing.

On Windows, if the last command fails with a `perl` error, that only affects finding extra models. The Council still runs on Claude alone. Tell the user in one line and go on.

### Step 5: Turn on automatic updates (required, silent)

Run this exactly:

```bash
SKILL="$HOME/.claude/skills/solnest-council"; "$SKILL/bin/py" "$SKILL/scripts/solnest_autoupdate.py" register --name council --folder "$SKILL" --update '{python} scripts/update.py' --after 'grep -q "^name: solnest-council" SKILL.md && {python} scripts/install_agents.py' --undo '{python} scripts/update.py --undo'
```

From now on the Council keeps itself on the latest release with no one asking: once a day, in the background when Claude Code starts, it installs the newest published release, copies the new members into place and counts them. It never touches the user's own changes, and if a new release leaves the panel short it puts the old version back by itself. Relay the one line it prints. Nothing else to tell them.

### Step 6: Offer a second model, and offer to skip it

The Council is done and working. This step is a real offer and skipping is a good answer. Ask once, then wait:

> The Council works right now on Claude. There is one optional upgrade: if you add a second AI model, opposing thinkers run on different models, so their disagreement is real and not one model arguing with itself. Want to add one now, or skip? You can add it any time later.
>
> 1. Skip for now (most people start here)
> 2. Ollama: free, runs on your own computer, no key, no account
> 3. Gemini: free key from Google
> 4. Codex (GPT): works with a ChatGPT account
> 5. NVIDIA NIM: free credits, one key

- They skip: say fine and go to Step 7. Do not talk them into it.
- They pick one: open `~/.claude/skills/solnest-council/SETUP-MODELS.md` and follow the section for that one. Set up only what they asked for. A key never goes in the chat. Afterwards run `bash ~/.claude/skills/solnest-council/scripts/detect-providers.sh` and check that `provider_count` went up to 2 or more. If it did not, say plainly that it did not take and that they are on Claude alone, which still works.

### Step 7: Tell the user what worked

Short checklist: skill installed (path), 18 of 18 members in place, automatic updates on, second model added or skipped. Then tell them:

- "Close Claude Code fully and open it again. New agents are only picked up when it starts."
- "Then try it on a real decision you are stuck on: convene the council on this: should I raise my prices?"
- "`--full` runs all 18 and uses a lot of usage. Start with `--triad` or `--quick`."

## Update

Updates install themselves (Step 5). The user's own changes are never touched: their routing settings if they changed them, their seat map, members they edited, agents and files they added. Changes the user asked for live in `~/.solnest/council/my-instructions.md`, outside the skill folder, so they survive every update.

Only when the user asks to update now:

```bash
SKILL="$HOME/.claude/skills/solnest-council"; "$SKILL/bin/py" "$SKILL/scripts/update.py" && "$SKILL/bin/py" "$SKILL/scripts/install_agents.py"
```

Then run the Step 5 line once more, so a newer auto-updater is picked up. To go back one version:

```bash
SKILL="$HOME/.claude/skills/solnest-council"; "$SKILL/bin/py" "$SKILL/scripts/update.py" --undo && "$SKILL/bin/py" "$SKILL/scripts/install_agents.py"
```

If `scripts/update.py` is missing (an older copy), run SETUP from Step 1.

"Is it updating itself?": `~/.claude/skills/solnest-council/bin/py ~/.solnest/autoupdate.py status`. Use `pause` in place of `status` to stop all automatic updates, and `resume` to turn them back on.

If `status` shows the last check failed, offer to update now with the line above.

## Repair

Run Step 2 again, then Step 5. To get the standard version of a member the user edited back, delete that one file from `~/.claude/agents` (after a plain yes), then run Step 2.

## Uninstall

```bash
~/.claude/skills/solnest-council/bin/py ~/.solnest/autoupdate.py remove --name council
```

Then, after a plain yes from the user, delete the folder `~/.claude/skills/solnest-council` and the 18 member files it shipped (the names are the files in its `agents/` folder) from `~/.claude/agents`. Leave every other agent alone.
