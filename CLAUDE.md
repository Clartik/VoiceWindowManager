# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A voice-controlled window manager for Windows 11. The goal: speak a command ("move Chrome to the second monitor", "dock this window left", "hide windows") and have the program open/close/move/dock windows and manage virtual desktops accordingly. This is an early-stage, single-user prototype — there is no build system, no test suite, no linter config, and no dependency manifest (`requirements.txt`/`pyproject.toml`) yet; dependencies are installed ad hoc via `pip`.

## Running the code

There's no orchestrated entry point yet — each file is currently runnable/testable in isolation:

- `python voice.py` — raw STT loop (prints live + final transcriptions from the mic, no command handling).
- `python main.py` — the intended orchestrator loop (STT → intent parsing → dispatch), but currently a stub: `execute_command` is defined but never called from the `while True` loop, and only handles `'exit'` inline.
- `python window.py` — exploratory `pywinctl` snippets (currently commented out).

Dependencies observed in use: `RealtimeSTT` (voice capture/transcription), `PyWinCtl` (cross-platform window control), `pydantic` (intent schema/validation). Intent parsing is planned to run through a **local Ollama model** (not a paid API) — Ollama must be installed and running (`ollama serve` runs as a background service on Windows) with a small instruct model pulled (e.g. `llama3.2:3b`) for that piece to work once wired up.

## Architecture

The intended data flow, split one file per concern:

```
voice.py (STT: mic → raw text)
   → intent.py (raw text → structured WindowIntent, via a local Ollama model)
      → window.py (WindowIntent → pywinctl calls)
         orchestrated by main.py
```

**Why a structured intent schema, not keyword matching:** free-form voice text is parsed into a fixed `WindowIntent` (pydantic model in `intent.py`) rather than matched with substring/keyword checks, so the dispatcher only ever has to handle a known, validated shape. The schema is passed to Ollama's structured-output (`format`) parameter so the model is constrained to emit valid JSON for this shape.

**`WindowIntent` fields and the reasoning behind them** (this isn't obvious from the schema alone — it was designed deliberately around Windows-specific distinctions):

- `action` — one of `open`, `close`, `minimize`, `move`, `dock`, `assign_desktop`, `switch_desktop`, `exit`, `unknown`.
  - `open` covers both "open X" and "show X" — the model doesn't know whether an app is already running; that check belongs in the **dispatcher**, which should look up existing windows first and focus/restore instead of relaunching.
  - `move` is monitor-to-monitor placement only. It is deliberately separate from `assign_desktop` (send a specific window to a different **virtual desktop**) and `switch_desktop` (change which virtual desktop is currently being **viewed** — no window target at all). These are distinct Windows operations and were kept as distinct actions rather than folded into one `move` with a type flag.
  - `dock` covers snapping into a fixed screen position (halves/quarters/`full`) and also absorbs directional phrasing like "move it left" — there is intentionally no separate freeform-nudge action.
  - `minimize`'s `target` accepts the literal string `"all"` (for "hide windows") in addition to a specific app/window name — this is a special-cased value, not a separate schema field.
  - `unknown` is the required fallback for anything ambiguous or unrelated, so misheard STT output doesn't force a guessed action.
- `target` — free text (app/window name), optional, `None` when the command implies the focused window.
- `destination` — free text used by `move`/`assign_desktop`/`switch_desktop` (e.g. monitor/desktop reference or `next`/`previous`). Kept as a string rather than an enum since desktop/monitor counts vary per machine; normalization (e.g. always emitting `next`/`previous`/a bare number) is intended to be handled via prompt instructions to the model, not the type system.
- `position` — a closed `Literal` enum (`left_half`, `right_half`, `top_half`, `bottom_half`, `top_left`, `top_right`, `bottom_left`, `bottom_right`, `full`), used only by `dock`. Kept as an enum (unlike `target`/`destination`) because the window-management code can only compute a fixed set of positions.

**Local LLM choice:** Ollama running a small instruct model (not a paid cloud API) was chosen deliberately — this program is meant to run continuously in the background, so it needed to avoid per-request cost, internet dependency, and rate limits. The intent-parsing task (classify into ~9 actions + extract 1-3 slots) is narrow enough that a 3B-7B local model is expected to be sufficient; this should be validated against real example commands before assuming a larger model is needed.

## Working in this repo

This is a personal/learning project — the user wants to build it themselves. **Do not write or edit code unless explicitly asked to.** Default to explaining architecture, walking through design tradeoffs, and letting the user write the implementation; only produce code when they directly request it (e.g. "write this", "show me an example").
