# 🏛️ Solnest Council — a free Claude skill from Solnest AI

---

## 🔄 Already installed? Here's how to update

Paste this whole line into **Claude Code** and send it:

> Update my Solnest Council. Follow the instructions at https://raw.githubusercontent.com/Solnest-AI/solnest-council/main/UPDATE.md exactly.

Claude pulls the latest version and refreshes all 18 members. **Any custom agents you've written are left alone** — the update only touches the 18 files it ships.

> **Claude, if you are reading this page because the user asked you to update this skill:** fetch and follow [`UPDATE.md`](UPDATE.md) in this repo, top to bottom. Note it installs to **two** locations — the skill folder *and* the agents folder.

---

Most AI gives you one opinion, delivered with total confidence.

This gives you **eighteen**, and they're designed to **disagree with each other on purpose.**

Convene a panel of history's sharpest thinkers on any hard call — Socrates, Aristotle, Feynman, Torvalds, Machiavelli, Sun Tzu, Marcus Aurelius, Lao Tzu, Ada Lovelace, Musashi, Alan Watts, Karpathy, Sutskever, Kahneman, Donella Meadows, Charlie Munger, Nassim Taleb, and Dieter Rams. They analyze, cross-examine each other, and come back with a reasoned verdict — **including where they couldn't agree.**

That last part is the whole point. When all 18 converge, you can move fast. When they split, that split *is* the answer you were missing.

Built by [Ryan Lefebvre](https://instagram.com/Ryan_Le5) / **Solnest AI**. Free to use. **No API keys, no accounts, nothing to pay for** — it runs on the Claude you already have.

---

## Why it isn't just "ask Claude 18 times"

The members are built in **polarity pairs** — thinkers who fundamentally disagree about how to think:

| | vs | | The tension |
|---|---|---|---|
| **Socrates** | vs | **Feynman** | Tear the assumptions down vs rebuild from first principles |
| **Torvalds** | vs | **Musashi** | Ship it today vs wait for the decisive moment |
| **Taleb** | vs | **Karpathy** | The hidden catastrophic tail vs the smooth empirical curve |
| **Kahneman** | vs | **Feynman** | *Your own reasoning is the first error* vs trust the reasoning |
| **Meadows** | vs | **Torvalds** | Redesign the system vs fix the symptom and move on |
| **Rams** | vs | **Ada** | What the user actually needs vs what the tech can do |

The Council **forces those pairs apart** so they can't collapse into one agreeable voice. You get real friction, not eighteen paraphrases of the same take.

---

## Install it

1. Download this repo (green **Code** button → **Download ZIP**) and unzip it.
2. Open **Claude Code**.
3. **Drag the unzipped folder** into the chat.
4. Say: **"Set this up."**

Claude reads [`START-HERE.md`](START-HERE.md) and handles it. Takes about a minute.

> ⚠️ **Claude Code, not the Claude Desktop app.** The Council works by spawning subagents, and the desktop app can't do that.

> 📁 **It installs to two places** — the skill itself, plus 18 agent files. The installer does both and verifies you got all 18. If you ever see it convene a partial panel, run the update and it'll repair itself.

---

## Using it

Start here — a real decision you're actually stuck on:

```
/solnest-council --triad strategy Should I raise my prices to $5k?
```

Or just say **"convene the council on this"** in plain English.

### The modes

| Command | What you get | When |
|---|---|---|
| `--quick <question>` | Fast, 2 rounds, no cross-examination | You want a gut-check |
| `--duo <question>` | **Two opposites argue it out** | The call is genuinely 50/50 |
| `--triad <domain> <question>` | Three thinkers picked for that domain | **Start here — the sweet spot** |
| `--full <question>` | All 18 | The decision is big enough to deserve it |
| `--members socrates,taleb,rams <q>` | Exactly who you want | You know who you need |

### The triads — pick the one that fits your problem

`strategy` · `shipping` · `product` · `founder` · `risk` · `decision` · `economics` · `design` · `systems` · `uncertainty` · `bias` · `architecture` · `debugging` · `ethics` · `innovation` · `conflict` · `complexity` · `ai` · `ai-product` · `ai-safety`

So: `/solnest-council --triad risk Should I put $50k into this?` pulls Sun Tzu, Aurelius, and Feynman — threats, resilience, and empirical verification.

> 💡 **`--full` spawns all 18 agents and uses real tokens.** It's not stuck — it's doing eighteen thinkers' worth of work. Save it for decisions that earn it. `--triad` handles 90% of what you'll throw at it.

---

## The 18 also work on their own

They're installed as regular agents, so you can call one directly without convening anything:

- **`council-taleb`** — a genuinely brutal tail-risk reviewer. "What kills this?"
- **`council-kahneman`** — audits *your* thinking for bias before you commit.
- **`council-munger`** — inverts the problem: what would guarantee failure?
- **`council-rams`** — cuts a design down to what the user actually needs.
- **`council-torvalds`** — tells you to ship it or shut up.

---

## Optional: give it more than one brain

**Skip this and the Council still works.** It runs on Claude alone, and that's how most people should start.

But here's the honest limitation of Claude-only: all 18 members are the same model wearing different hats. They argue — genuinely — but it's one mind playing every part.

Add a second model and that changes. The Council takes each **polarity pair** and puts the two halves on **different engines**: Socrates on one, Feynman on another. Taleb and Karpathy on separate models. The disagreement stops being simulated.

The installer offers to set this up and **offers to skip it** — no pressure either way. You can add it any time later. Cheapest path is **Ollama**: free, local, no key, no account.

Full walkthrough: **[`SETUP-MODELS.md`](SETUP-MODELS.md)** — covers Ollama, Gemini, Codex, and NVIDIA NIM.

To see who's running on what, without spending anything:

```
/solnest-council --dry-route --full <any question>
```

> ⚠️ **The Council uses the `codex` / `gemini` CLI tools — not the Claude Code plugins.** If you installed [Solnest Three-Brain](https://github.com/Solnest-AI/solnest-three-brain), that gave you the *plugins*, which is a different thing. Some overlap, but don't assume. `SETUP-MODELS.md` has a one-line check that tells you exactly what the Council can see.

---

## Nothing of yours leaves your machine

The Council reads nothing, stores nothing, and phones nobody. It's text and agents, running in your Claude.
