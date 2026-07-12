# Adding more brains to the Council (optional)

**You don't need this.** The Council works perfectly on Claude alone — 18 members, all modes, no keys, nothing to pay for. If you're here to get started, close this file and go use it.

This is for when you want the Council to be **genuinely** multi-minded.

---

## Why you'd bother

By default all 18 members are Claude. They're given sharply different personalities and instructions, and they *do* disagree — but underneath, it's one model arguing with itself.

Add a second or third model and the Council does something it can't otherwise do: it takes each **polarity pair** — the thinkers built to oppose each other — and **puts them on different models.** Socrates runs on one, Feynman on another. Taleb and Karpathy end up on separate engines.

Now the disagreement is real. It isn't one model playing both parts.

**The Council figures this out on its own.** Install a model, and it's detected and used the next time you convene. There's nothing to configure and no config file to edit.

---

## What it looks for

The Council runs `scripts/detect-providers.sh`, which checks whether these **command-line tools are installed and working**:

| Provider | What it needs | Cost |
|---|---|---|
| **Claude** | Already there | Included |
| **Ollama** | The `ollama` command + at least one model pulled | **Free, runs on your machine** |
| **Gemini** | The `gemini` command + a `GEMINI_API_KEY` | Free tier |
| **Codex (GPT)** | The `codex` command + a ChatGPT login | Free tier works |
| **NVIDIA NIM** | An `NVIDIA_API_KEY` | Free credits |

> ⚠️ **These are the CLI tools, not the Claude Code plugins.** If you installed [Solnest Three-Brain](https://github.com/Solnest-AI/solnest-three-brain), that set up the *plugins* — a different thing. The Council needs the actual `codex` / `gemini` commands on your PATH. Some overlap, but don't assume one gives you the other. Run the check at the bottom of this page to see what you really have.

**Pick one and stop.** Two providers already gets you real cross-model friction. You do not need all of them.

---

## Option A — Ollama (start here)

The best first choice: **completely free, no key, no account, no rate limit.** The models run on your own machine.

1. Install it from **[ollama.com/download](https://ollama.com/download)** (or `brew install ollama` on a Mac).
2. Pull a model with some reasoning ability:
   ```bash
   ollama pull qwen3-coder
   ```
3. Make sure it's running:
   ```bash
   ollama list
   ```
   If that prints your model, you're done. The Council will find it.

The tradeoff: local models are smaller, so those council seats are less sharp than the Claude ones. For *generating genuine disagreement* that's fine — often better, because a different architecture fails differently, which is exactly the point.

---

## Option B — Gemini CLI

1. Install it:
   ```bash
   npm install -g @google/gemini-cli
   ```
2. Get a free API key at **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)** (no credit card).
3. Set it so it survives a restart:

   **macOS (zsh):**
   ```bash
   echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```
   **Linux (bash):** same, but `~/.bashrc`.
   **Windows (PowerShell):**
   ```powershell
   setx GEMINI_API_KEY "your-key-here"
   ```

### 🚨 Do not skip the key

**Signing in with a Google account no longer works** — the API key is the only way in. Older guides still tell you to run `gemini` and sign in. Ignore them.

And here's the trap: the Council detects Gemini by checking that the `gemini` command *runs* — **it does not check whether you're logged in.** So if you install the CLI and skip the key, the Council will happily hand council seats to Gemini, and **those members will fail in the middle of a deliberation.**

**So: either set the key, or don't install the CLI at all.** Half-installed is the one state that actually breaks things.

Verify:
```bash
gemini --version && echo "key set: ${GEMINI_API_KEY:+yes}"
```
You want a version number **and** `key set: yes`.

---

## Option C — Codex CLI (GPT)

1. Install it:
   ```bash
   npm install -g @openai/codex
   ```
2. Sign in:
   ```bash
   codex login
   ```
   Works with **any ChatGPT account, including the free tier**, or an OpenAI API key. It opens a browser.

Verify:
```bash
codex --version
```

---

## Option D — NVIDIA NIM

Gives you access to several large open models (DeepSeek, Qwen, Kimi) through one key.

1. Get a key at **[build.nvidia.com](https://build.nvidia.com)** — free credits, no card.
2. Set it (it must start with `nvapi-`):
   ```bash
   echo 'export NVIDIA_API_KEY="nvapi-your-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

Unlike the others, NIM needs no CLI — the key alone is enough.

---

## Check what the Council can actually see

This is the source of truth. Run it:

```bash
bash ~/.claude/skills/solnest-council/scripts/detect-providers.sh
```

You'll get JSON. Look at **`provider_count`**:

- **`1`** — Claude only. The Council runs Claude-only. Working as intended.
- **`2` or more** — multi-model is live. Polarity pairs will be split across engines.

To see the actual assignments without running a deliberation:

```
/solnest-council --dry-route --full Should we rewrite this in Rust?
```

That prints the routing table — member → provider → model — and stops. **It's the fastest way to confirm your setup did what you think it did.**

---

## Turning it off

Don't want multi-model on a particular question? Add `--no-auto-route` and it runs Claude-only for that run:

```
/solnest-council --no-auto-route --triad strategy Should I raise prices?
```

To turn it off permanently, uninstall the CLI or unset the key. There's no config to undo.

---

## Your keys are yours

Every key lives in **your** shell profile, on your machine. None of them are ever written into this skill folder, and nothing here phones home.
