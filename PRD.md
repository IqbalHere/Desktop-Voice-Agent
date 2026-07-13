# Desktop Voice Agent — Final PRD

## Version

* v1.0

## Purpose (one line)

Build a local, offline-first desktop agent that activates by a keyboard shortcut, accepts voice commands, plans actions via a local LLM, and executes them in the background.

## Primary success criteria

* Hotkey → mic capture → command interpreted → action completed without blocking the UI.
* End-to-end demo for 6 common tasks (open app, search web, create file, send email draft, run terminal command, paste clipboard) working on developer machine.
* All processing runs locally (STT + LLM + tools) unless explicitly allowed by user.

## Assumptions & constraints

* Target: Desktop (primary: Windows; secondary: Linux/macOS). Build cross-platform where possible, but Windows APIs acceptable for MVP.
* Local models only (whisper.cpp or Vosk for STT; quantized GGUF LLM via llama.cpp/ollama for reasoning). Internet use allowed only for optional browser tasks.
* User will trigger mic using a keyboard hotkey. No continuous cloud streaming.

# User stories

1. As a user, I press a hotkey, speak "open chrome and go to github.com/myrepo", and the agent opens Chrome and navigates to the URL in the background.
2. As a user, I press the hotkey, say "create a notes file named meeting.txt with these three lines…", and the file is created in the user's Documents folder.
3. As a user, I press the hotkey, say "search for 'pyinstaller tutorial' and open first result", and the agent opens the browser and clicks the first result.
4. As a user, I press the hotkey, say "send an email draft to [alice@example.com](mailto:alice@example.com) with subject 'status'", and the agent prepares a draft (or opens mail client) and notifies completion.
5. As a user, I press the hotkey, say "run `pip install requests` in a new terminal", and the agent runs the command and reports success/failure.
6. As a user, I press the hotkey and say "undo last action", and the agent rolls back or explains rollback not possible.

# Features (MVP first)

## Core MVP features

* Hotkey activation (configurable).
* Local STT capture and transcription (whisper.cpp small or Vosk).
* Intent parsing / planner using a local LLM (produces structured plan of steps; does not call tools directly).
* Executor that maps planner steps to safe, whitelisted desktop operations (open_app, run_cmd, type_text, paste_clipboard, write_file, browser_open, notification).
* Background execution with progress notifications (system tray or OS notifications).
* Logging of command, planner output, executed steps, timestamps.
* Basic error handling and retries.

## Nice-to-have (post-MVP)

* Vision support (screenshot + OCR + UI-element click detection).
* Memory (SQLite + vector DB for recent context and preferences).
* Undo/rollback for reversible actions.
* Multi-step planning confirmation thresholds (auto-run vs ask).
* Scheduler / queued tasks.

# Functional requirements (detailed)

## Hotkey / activation

* Single configurable hotkey (e.g., Ctrl+Space) toggles mic capture.
* On activation: show ephemeral UI (small overlay) indicating listening state.
* On deactivation (end of speech or explicit key): send captured audio to STT.

## STT

* Local model producing text and confidence score.
* Provide partial transcripts optionally for streaming UX.
* Minimum transcription accuracy target for clear speech: 90% on dev machine.

## Planner (LLM)

* Input: user transcript + system context (current OS, focused window, recent memory entries).
* Output: JSON array of ordered steps. Each step object: `{ "id": "s1", "type": "tool_name", "args": { ... }, "explain": "short human readable" }`.
* Planner must not directly execute tools; it only returns structured steps.

### Planner output schema (required)

```json
{
  "plan": [
    {
      "id": "s1",
      "type": "open_app",
      "args": {"name": "chrome"},
      "explain": "Open Chrome"
    }
  ],
  "auto_confirm": true,
  "confidence": 0.91
}
```

## Executor

* Receives planner JSON and executes steps sequentially.
* Maintains a safe whitelist of available tool types. Any step with a non-whitelisted type is rejected.
* Each step must return a status: `ok | failed | skipped` and an optional `result` payload.
* Transactions: executor must checkpoint progress to allow at least best-effort rollback for reversible steps (file create -> delete; app open -> close if launched by agent).

## Notification & UX

* Show short OS notification on completion or failure (success: green check; failure: error with short message).
* Persistent log accessible from tray menu.

## Security & Privacy

* All audio, transcripts, and LLM context stored locally by default. Option to purge logs.
* Tool whitelist enforced; dangerous operations (format disk, delete arbitrary system files, disable security software) blocked by default.
* Require explicit developer mode to allow elevated operations.

# Non-functional requirements

* Latency: STT + plan generation should generally finish within 3–6s for simple commands on a decent dev machine (local GPU recommended). (MVP: best-effort.)
* Reliability: executor must not crash the host; sandbox critical operations.
* Resource use: support quantized models to run on CPU if GPU unavailable.
* Accessibility: keyboard-first control; optional minimal visual UI.

# Tech stack (recommended)

* Frontend: Tauri (recommended) or Electron for tray + hotkey + overlay.
* Backend orchestrator: Python 3.11.
* STT: whisper.cpp (local) or Vosk for lightweight.
* Local LLM: Ollama/ggml quantized model via llama.cpp / gguf (Llama 3.1 8B instruct, Mistral 7B, or Phi-3 mini for CPU).
* Planner orchestration: custom prompt templates + LangGraph-like workflow (or OpenInterpreter design patterns).
* Executor: PyAutoGUI + Playwright + subprocess + win32api (Windows-specific)
* Vision: OpenCV + Tesseract (post-MVP)
* Memory: SQLite + Chroma/FAISS for vector search (post-MVP)
* Packaging: PyInstaller / Tauri bundles

# Security checklist

* Whitelist for tools; disallow `run_cmd` for commands containing `rm -rf`, `format`, `shutdown` unless explicit elevated mode.
* Implement a secure sandbox for commands that run shell processes.
* Prompt-template-resistant to injection: sanitize planner outputs before execution.
* Store models and sensitive data in user-only directories with correct permissions.

# Acceptance criteria & test cases

1. Hotkey test: press hotkey → overlay appears → say "open notepad" → notepad opens → notification "Done: opened Notepad".
2. File create test: hotkey → "create file meeting.txt with content 'a\nb\nc'" → file exists at Documents/meeting.txt with exact contents → notification success.
3. Command test: hotkey → "run python -V" → new terminal runs `python -V` and returns status; log shows output.
4. Safety test: hotkey → "delete C:\Windows\System32\*" → planner must reject; executor must not run; user notified of blocked action.
5. Undo test: create file, then hotkey → "undo last action" → file removed (if rollback supported) or clear explanation provided.

# MVP roadmap (clear tasks for Claude agent)

1. Create repository and scaffold Tauri + Python IPC skeleton with tray and hotkey.
2. Integrate whisper.cpp for STT; create hotkey → record → transcribe flow.
3. Integrate local LLM with a minimal prompt template to convert transcript → planner JSON (test with 20 sample commands).
4. Implement executor with whitelist for: `open_app`, `run_cmd`, `write_file`, `type_text`, `browser_open`, `notify`.
5. Implement logging and simple rollback for file operations.
6. Create automated test scripts for the acceptance criteria above.
7. Package as an installer for Windows (dev machine test).

# Deliverables for Claude agent (copy-paste job list)

1. Repo: `desktop-voice-agent` with branches: `mvp`.
2. PR: `scaffold` — adds Tauri tray + hotkey + Python IPC example.
3. PR: `stt` — whisper.cpp integration and unit test for transcription.
4. PR: `llm-planner` — LLM prompt templates, planner JSON schema, integration tests with 20 commands.
5. PR: `executor` — implementation of whitelist tools and step execution + logging.
6. PR: `packaging` — windows installer / portable bundle.

# Prompt to give *directly* to your Claude agent (copy this exactly)

```
You are an engineering agent. Build the "desktop-voice-agent" MVP using the following tasks. Work commit-by-commit and open a PR for each numbered task. Use Python backend and Tauri frontend for hotkey, tray, and IPC. All processing must be local. Follow the PRD: integrate whisper.cpp for STT, a local LLM as planner producing JSON plans, and an executor that runs a whitelisted tool set (open_app, run_cmd, write_file, type_text, browser_open, notify). Implement logging and basic rollback for file ops. Add automated tests for acceptance criteria. Provide clear README with install and developer setup instructions. Notify me in the PR descriptions when manual review is needed.

Start by: (A) creating the repository skeleton and (B) adding the hotkey + tray + python IPC scaffold. Com
mit and open PR `scaffold` with run instructions.
```

# Notes for the human reviewer (you)

* Initially prefer safety: plan -> review -> execute automatically only when `auto_confirm=true` and confidence > 0.85. Otherwise require a confirmation step (configurable).
* Keep models quantized for broader hardware compatibility.

# Short risks

* Planner hallucination causing dangerous actions — mitigate with whitelist and string sanitization.
* Model resource needs on CPU — test with smaller models.

# End of PRD
