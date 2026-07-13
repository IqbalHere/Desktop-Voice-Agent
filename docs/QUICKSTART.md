# Quick Start Guide - Desktop Voice Agent Scaffold

## What This PR Delivers

This scaffold provides the foundational infrastructure for the Desktop Voice Agent:

1. **Tauri Application** - Cross-platform desktop app framework
2. **Global Hotkey** - Press `Ctrl+Space` to trigger (currently shows notification)
3. **System Tray** - Always-accessible menu in system tray
4. **Python Backend** - IPC-ready orchestrator (currently logs to console)
5. **Settings UI** - Modern web-based settings interface

## Running the Application

### Prerequisites

Install these tools first:
- Node.js 16+ (for Tauri frontend)
- Rust (latest stable)
- Python 3.11+

### Linux Additional Requirements

```bash
sudo apt-get install -y libwebkit2gtk-4.1-dev libgtk-3-dev \
    libayatana-appindicator3-dev librsvg2-dev patchelf
```

### Quick Start

```bash
# 1. Install dependencies
npm install
pip install -r requirements.txt

# 2. Run the application
npm run dev
```

### What You'll See

1. **Console Output**:
   - "Desktop Voice Agent Backend - MVP Scaffold"
   - "Backend started successfully!"
   - "Desktop Voice Agent started!"
   - "Press Ctrl+Space (or Cmd+Space on macOS) to trigger voice capture"

2. **System Tray Icon**:
   - Look for a purple microphone icon in your system tray
   - Right-click to see menu: Trigger, Settings, View Logs, Quit

3. **Hotkey Test**:
   - Press `Ctrl+Space` (or `Cmd+Space` on macOS)
   - You should see a notification: "Listening... Press Ctrl+Space again to stop"

4. **Settings Window**:
   - Click "Settings" in tray menu
   - Opens a window showing status, quick start guide, and test buttons

## Testing the Scaffold

### 1. Backend Test
```bash
python3 backend/main.py
# Should output: "Desktop Voice Agent Backend - MVP Scaffold"
# Press Ctrl+C to stop
```

### 2. Run Python Tests
```bash
pytest tests/ -v
# Should show: 6 passed
```

### 3. Check Rust Compilation
```bash
cd src-tauri && cargo check
# Should show: "Finished `dev` profile [unoptimized + debuginfo]"
```

## Project Structure

```
Desktop-Voice-Agent/
├── frontend/           # Tauri frontend UI (HTML)
├── src-tauri/          # Rust application (hotkey, tray, IPC)
│   ├── src/main.rs     # Main application logic
│   ├── icons/          # Application icons
│   └── Cargo.toml      # Rust dependencies
├── backend/            # Python backend (STT, LLM, executor - to be added)
│   └── main.py         # Backend orchestrator
├── tests/              # Test suite
├── README.md           # Full documentation
└── PRD.md              # Product requirements
```

## Current Functionality

### What Works Now
- ✅ Global hotkey registration (Ctrl+Space)
- ✅ System tray with menu
- ✅ Notification system
- ✅ Python backend process spawning
- ✅ IPC infrastructure (frontend ↔ Python)
- ✅ Settings window UI
- ✅ Cross-platform support

### What's Coming Next
- 🔜 Audio recording and STT (whisper.cpp)
- 🔜 LLM planner integration
- 🔜 Command executor with whitelisted tools
- 🔜 Logging and rollback
- 🔜 Comprehensive tests

## Troubleshooting

### "Backend: Not Running" in Settings

The Python backend may fail to start if:
- Python 3.11+ is not in PATH
- `python3` command is not available (try `python` instead)

**Fix**: Edit `src-tauri/src/main.rs` line ~75 to use `python` instead of `python3`

### Hotkey Not Working

- Check if another app uses Ctrl+Space
- On Linux, ensure you have permissions for global hotkeys
- Try a different key combination (edit src-tauri/src/main.rs)

### Build Errors on Linux

Ensure you have all dependencies:
```bash
sudo apt-get install -y libwebkit2gtk-4.1-dev libgtk-3-dev \
    libayatana-appindicator3-dev librsvg2-dev patchelf
```

## Architecture Notes

### IPC Flow (Ready for Implementation)
```
User → Hotkey → Tauri → Python Backend → (Future: STT → LLM → Executor)
                   ↓
             Notification
```

### Python Backend
- Runs as a child process of Tauri app
- Communicates via stdin/stdout (JSON)
- Ready for STT and LLM integration

### Future Enhancements
Each will come in its own PR:
1. `stt` - Speech-to-text with whisper.cpp
2. `llm-planner` - Local LLM integration
3. `executor` - Tool execution engine
4. `packaging` - Distributable bundles

## Next Steps

1. ✅ Test the scaffold on your machine
2. ✅ Verify all components work
3. ✅ Confirm hotkey, tray, and notifications work
4. 🔜 Proceed to STT integration PR

---

**Status**: ✅ Scaffold Complete
**Branch**: `copilot/scaffold-repo-skeleton-and-ipc`
**Next PR**: STT Integration (whisper.cpp)
