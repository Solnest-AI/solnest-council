# Solnest Council

A Solnest AI Skool tool for Claude Code.

Most AI gives you one opinion, said with total confidence. This gives you eighteen, and they are built to disagree with each other on purpose. Put a hard decision in front of a panel of history's sharpest thinkers (Socrates, Feynman, Torvalds, Machiavelli, Taleb, Kahneman, Munger, Rams and ten more). They work on it, question each other, and come back with one verdict, including where they could not agree.

When they all land in the same place, you can move fast. When they split, the split is the answer you were missing.

## What you need

- Claude Code (desktop app or terminal), logged in. The plain Claude chat app will not work: the Council runs each thinker as its own agent, and only Claude Code can do that.
- No accounts, no API keys, no cost beyond your normal Claude plan.
- Optional, later: a second AI model (Ollama is free), so opposing thinkers run on different models. See "More than one brain" below.

## Set it up in 3 steps

1. Copy this page's link.
2. Paste it into Claude Code and say: **set this up**
3. Close Claude Code fully, open it again, and try it on a real decision you are stuck on. Say: **convene the council on this: should I raise my prices?**

## Using it

Say "convene the council on this" in plain words, or use the command:

```
/solnest-council --triad strategy Should I raise my prices to $5k?
```

| Command | What you get | When |
|---|---|---|
| `--quick <question>` | Fast, two rounds, no cross-questions | You want a gut check |
| `--duo <question>` | Two opposites argue it out | The call is truly 50/50 |
| `--triad <domain> <question>` | Three thinkers picked for that kind of problem | Start here |
| `--full <question>` | All 18 | The decision is big enough to earn it |
| `--members socrates,taleb,rams <question>` | Exactly who you want | You know who you need |

The triads: `strategy`, `shipping`, `product`, `founder`, `risk`, `decision`, `economics`, `design`, `systems`, `uncertainty`, `bias`, `architecture`, `debugging`, `ethics`, `innovation`, `conflict`, `complexity`, `ai`, `ai-product`, `ai-safety`.

`--full` runs all 18 thinkers and uses a lot of your Claude usage. It is not stuck, it is doing eighteen thinkers' worth of work. `--triad` covers most of what you will throw at it.

## Why it is not just "ask Claude 18 times"

The members come in pairs that disagree about how to think:

| | vs | | The tension |
|---|---|---|---|
| **Socrates** | vs | **Feynman** | Tear the assumptions down vs rebuild from first principles |
| **Torvalds** | vs | **Musashi** | Ship it today vs wait for the right moment |
| **Taleb** | vs | **Karpathy** | The hidden disaster vs the smooth trend line |
| **Kahneman** | vs | **Feynman** | Your own reasoning is the first error vs trust the reasoning |
| **Meadows** | vs | **Torvalds** | Redesign the system vs fix the symptom and move on |
| **Rams** | vs | **Ada** | What the user needs vs what the tech can do |

The Council keeps those pairs apart, so you get real friction and not eighteen versions of the same take.

## The 18 also work on their own

They install as regular agents, so you can call one without convening anything:

- `council-taleb`: a hard reviewer of what could go badly wrong. "What kills this?"
- `council-kahneman`: checks your own thinking for bias before you commit.
- `council-munger`: turns the problem around. What would guarantee failure?
- `council-rams`: cuts a design down to what the user needs.
- `council-torvalds`: tells you to ship it.

## More than one brain (optional)

Skip this and the Council still works. On Claude alone, all 18 members are the same model wearing different hats. Add a second model and the Council puts each opposing pair on different models, so the disagreement is real. Setup offers this once and is happy to skip it. The cheapest way is Ollama: free, runs on your own computer, no key, no account. The full guide is in [SETUP-MODELS.md](SETUP-MODELS.md). Ask Claude "add a second model to my council" any time.

## Good to know

- Updates install themselves. Once a day, when Claude Code starts, the tool quietly moves to the newest release. You never have to ask.
- An update never wipes your own changes. Changes you asked Claude to make to how the Council works, routing settings you changed, any member you edited and any agent you added all stay exactly as they are.
- Want it to work differently? Just tell Claude ("always end the verdict with one next step for this week"). It remembers.
- The Council reads nothing, stores nothing and sends nothing anywhere. It is text and agents running in your Claude.
- Installed the Council before this version? Do the 3 steps above once. Your copy is brought up to date, your settings are kept, and from then on it updates itself.

## Credit

The Council is built on the open-source [council-of-high-intelligence](https://github.com/0xNyk/council-of-high-intelligence) project by nyk, used under the MIT license (kept in [LICENSE](LICENSE)). Solnest AI added the one-step setup, the multi-model guide and the automatic updates. From [Ryan Lefebvre](https://instagram.com/Ryan_Le5) and Solnest AI.

## Support

hello@solnestai.com

---

Claude: someone pasted this link and said "set this up" (or asked to update their Solnest Council). Read [CLAUDE.md](https://raw.githubusercontent.com/Solnest-AI/solnest-council/main/CLAUDE.md) in this repo and follow its SETUP section, one step per message. You run every command yourself. This tool needs no keys.
