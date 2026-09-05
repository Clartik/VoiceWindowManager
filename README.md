# VoiceWindowManager

A voice-controlled window manager for Windows 11. Speak a command and it opens, closes, minimizes, maximizes, restores, or docks windows — and (eventually) moves them between monitors and virtual desktops.

This is a personal/learning project and a work in progress — see [Current status](#current-status) for what's actually wired up today.

## How it works

```
voice.py   mic audio -> transcribed text (RealtimeSTT)
   |
   v
intents.py transcribed text -> structured WindowIntent (local Ollama model)
   |
   v
window.py  WindowIntent -> pywinctl calls (the actual window actions)
   |
   v
main.py    orchestrates the loop above, plus confirmation flow for destructive actions
```

Voice commands are never keyword-matched. Instead, a local LLM (via [Ollama](https://ollama.com)) parses free-form speech into a fixed JSON shape (`WindowIntent`) — an `action` plus a few optional slots (`target`, `destination`, `position`) — so the rest of the program only ever has to handle a known, validated structure. Ollama runs the model locally and for free, which matters since this is meant to run continuously in the background.

## Current status

**Working:**
- `close` — with a spoken yes/no confirmation before actually closing (destructive action, so it double-checks)
- `restore` — bring a minimized/maximized window back to normal size
- `dock` with `position: "empty"` — minimize (a specific app, the focused window, or `"all"`)
- `dock` with `position: "full"` — maximize (same target options), including restoring the most recently minimized window if no target is found
- `exit` — stop the program

**Not yet wired up (parsed by the model, but no dispatcher behind them yet):**
- `open` — launch or focus an app
- `move` — reposition a window onto a different monitor
- `dock` with an actual snap position (`left_half`, `top_right`, etc.) — real screen-quadrant docking
- `assign_desktop` / `switch_desktop` — virtual desktop support (likely needs a separate library, since Windows doesn't expose this through a public API that `pywinctl` covers)

## Setup

1. **Install [Ollama](https://ollama.com)** and pull a small instruct model:
   ```
   ollama pull llama3.2:3b
   ```
2. **Create a virtual environment** (Python 3.12 — `RealtimeSTT`'s dependencies are pickiest about version compatibility here):
   ```
   py -3.12 -m venv venv
   venv\Scripts\Activate.ps1
   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Running it

```
python main.py
```

Say a command like:
- "close this" (asks "are you sure?" first — reply yes/no)
- "minimize" / "hide this window" / "hide notepad" / "hide windows"
- "maximize" / "show this window"
- "restore this" / "restore notepad"
- "exit" (stops the program)

## Project structure

- `voice.py` — standalone speech-to-text loop (useful for testing STT in isolation)
- `intents.py` — the `WindowIntent` schema and `parse_intent`, which sends transcribed text + the system prompt to Ollama and returns a validated intent
- `window.py` — `WindowsManager`, the dispatcher that turns a `WindowIntent` into actual `pywinctl` calls
- `main.py` — `VoiceAgent`, the main loop tying STT, intent parsing, and dispatch together, plus the confirmation state machine for `close`
- `prompts/system_prompt.md` — the versioned system prompt that teaches the model the action set and how to normalize slots (monitor/desktop references, etc.)

See `CLAUDE.md` for a deeper dive into the design decisions behind the schema and why certain actions are split the way they are.
