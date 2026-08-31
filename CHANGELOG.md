# Changelog

## 1.1.1

- Added a `LICENSE` (MIT) — the README said "free to use" with no licence file to
  back it, which leaves anyone reusing the Council guessing.
- Reworded a personal operating note that had leaked into a shipped config file
  (`configs/auto-route-defaults.yaml`) into a neutral rationale comment.


## 1.1.0

- **The installer now offers to set up extra models — and offers to skip.** Adding a second engine lets the Council split opposing thinkers (Socrates vs Feynman, Taleb vs Karpathy) across *different* models, so the disagreement is real instead of one model arguing with itself. Skipping is fine; the Council works on Claude alone.
- New `SETUP-MODELS.md` — walkthroughs for Ollama (free, local, no key), Gemini, Codex, and NVIDIA NIM. Add one any time.
- Documented a trap worth knowing: the Council detects Gemini by checking the `gemini` command runs, **not** whether you're signed in. A Gemini CLI installed without a `GEMINI_API_KEY` gets council seats assigned to it and fails mid-deliberation. Set the key or don't install the CLI.
- Clarified that the Council uses the `codex`/`gemini` **CLI tools**, not the Claude Code plugins that Solnest Three-Brain installs.

## 1.0.0

- First public release.
- An 18-member panel of historical thinkers — Socrates, Aristotle, Feynman, Torvalds, Machiavelli, Sun Tzu, Aurelius, Lao Tzu, Ada Lovelace, Musashi, Watts, Karpathy, Sutskever, Kahneman, Meadows, Munger, Taleb, and Rams — that deliberate a problem and return a reasoned verdict, including where they disagreed.
- Modes: `--quick`, `--duo` (two opposites argue it out), `--triad` (3 members picked for your domain), `--full` (all 18), or hand-pick with `--members`.
- 20 predefined triads mapped to domains: strategy, shipping, risk, decision, economics, design, architecture, ai-safety, and more.
- **Runs on Claude alone — no API keys, no accounts.** If you also have Codex, Gemini, or Ollama installed, it detects them and spreads opposing thinkers across different models so they can't converge into one voice.
- All 18 members also work standalone as regular agents.
