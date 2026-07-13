# Desktop Voice Agent 🎤

A local, offline-first desktop agent that activates by keyboard shortcut, accepts voice commands, plans actions via a local LLM, and executes them in the background.

## 🌟 Features (MVP Scaffold)

This is the initial scaffold PR that includes:

- ✅ **Global Hotkey**: Press `Ctrl+Space` (or `Cmd+Space` on macOS) to trigger voice capture
- ✅ **System Tray**: Persistent tray icon with menu for easy access
- ✅ **Python Backend**: IPC-enabled backend ready for STT and LLM integration
- ✅ **Cross-platform**: Built with Tauri for Windows, macOS, and Linux support
- ✅ **Local Processing**: All processing runs locally (no cloud dependencies)

### Coming in Future PRs

- 🔜 **Speech-to-Text**: whisper.cpp integration for local transcription
- 🔜 **LLM Planner**: Local LLM for intent parsing and plan generation
- 🔜 **Task Executor**: Whitelisted tools (open_app, run_cmd, write_file, etc.)
- 🔜 **Logging & Rollback**: Comprehensive logging and file operation rollback
- 🔜 **Tests**: Automated tests for acceptance criteria

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16 or later) - [Download](https://nodejs.org/)
- **Rust** (latest stable) - [Install](https://rustup.rs/)
- **Python** 3.11 or later - [Download](https://www.python.org/)

### Platform-Specific Requirements

#### Windows
- Visual Studio Build Tools or Visual Studio with C++ development tools
- WebView2 (usually pre-installed on Windows 10/11)

#### macOS
- Xcode Command Line Tools: `xcode-select --install`

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev \
    build-essential \
    curl \
    wget \
    file \
    libxdo-dev \
    libssl-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/IqbalHere/Desktop-Voice-Agent.git
cd Desktop-Voice-Agent
```

### 2. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies (optional for scaffold)
pip install -r requirements.txt
```

### 3. Run in Development Mode

```bash
# Start the application in development mode
npm run dev
```

This will:
1. Start the Python backend (if available)
2. Launch the Tauri application
3. Register the global hotkey (`Ctrl+Space`)
4. Show the system tray icon

### 4. Test the Application

- **Access Settings**: Click the tray icon and select "Settings"
- **Test Hotkey**: Press `Ctrl+Space` (or `Cmd+Space` on macOS) - you should see a notification
- **Test Backend**: Click "Test Backend" in the settings window

## 🛠️ Development

### Project Structure

```
Desktop-Voice-Agent/
├── frontend/              # Tauri frontend UI
│   └── index.html        # Main settings/UI page
├── src-tauri/            # Tauri application (Rust)
│   ├── src/
│   │   └── main.rs       # Main app logic, hotkey, tray, IPC
│   ├── icons/            # Application icons
│   ├── Cargo.toml        # Rust dependencies
│   └── tauri.conf.json   # Tauri configuration
├── backend/              # Python backend
│   └── main.py           # Backend orchestrator (IPC server)
├── tests/                # Test suite (to be added)
├── docs/                 # Documentation
├── package.json          # Node.js dependencies
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Building for Production

```bash
# Build the application
npm run build
```

This will create a distributable application in `src-tauri/target/release/bundle/`.

### Running Tests

```bash
# Python tests (when implemented)
pytest tests/

# Frontend tests (placeholder)
npm test
```

## 🎯 Usage

### Global Hotkey

The default hotkey is `Ctrl+Space` (Windows/Linux) or `Cmd+Space` (macOS).

**Current Behavior** (Scaffold MVP):
- Press the hotkey → Shows a notification saying "Listening..."
- This demonstrates the hotkey registration and notification system

**Future Behavior** (Full MVP):
- Press the hotkey → Starts audio recording
- Speak your command → Transcribed via whisper.cpp
- Release or press again → Sends to LLM planner
- Plan is generated and executed automatically

### System Tray

The tray icon provides quick access to:
- **Trigger Voice Capture**: Manual trigger alternative to hotkey
- **Settings**: Open the settings window
- **View Logs**: Access application logs (coming soon)
- **Quit**: Exit the application

## 🔧 Configuration

### Hotkey Customization

Currently, the hotkey is hardcoded to `Ctrl+Space`. To change it:

1. Edit `src-tauri/src/main.rs`
2. Find the line: `app.global_shortcut().register("CommandOrControl+Space")`
3. Change to your preferred key combination (e.g., `"CommandOrControl+Shift+V"`)
4. Rebuild the application

Future versions will support runtime hotkey configuration.

## 📝 Logging

- **Backend Logs**: `backend.log` (created in the project root when backend runs)
- **Tauri Logs**: Visible in the terminal when running `npm run dev`

## 🐛 Troubleshooting

### Backend Not Starting

**Symptom**: Settings window shows "Backend: Not Running"

**Solutions**:
1. Ensure Python 3.11+ is installed: `python3 --version`
2. Check the console output for error messages
3. Try running the backend manually: `python3 backend/main.py`

### Hotkey Not Working

**Solutions**:
1. Check if another application is using the same hotkey
2. On Linux, ensure you have the necessary permissions
3. Try a different key combination
4. Check the console for error messages

### Build Errors

**Common Issues**:
- Missing dependencies: Re-run `npm install`
- Rust compilation errors: Update Rust with `rustup update`
- Python errors: Ensure Python 3.11+ is installed

## 🗺️ Roadmap

### ✅ Phase 1: Scaffold (Current PR)
- [x] Tauri application setup
- [x] Global hotkey registration
- [x] System tray implementation
- [x] Python backend IPC scaffold
- [x] Basic UI
- [x] README and documentation

### 🔜 Phase 2: STT Integration
- [ ] whisper.cpp integration
- [ ] Audio recording functionality
- [ ] Transcription pipeline
- [ ] Confidence scoring

### 🔜 Phase 3: LLM Planner
- [ ] Local LLM integration (Ollama/llama.cpp)
- [ ] Prompt templates
- [ ] JSON plan generation
- [ ] Plan validation

### 🔜 Phase 4: Executor
- [ ] Whitelisted tools implementation
- [ ] Step-by-step execution
- [ ] Progress notifications
- [ ] Error handling

### 🔜 Phase 5: Logging & Rollback
- [ ] Comprehensive logging
- [ ] File operation checkpointing
- [ ] Rollback mechanism
- [ ] Undo command

### 🔜 Phase 6: Testing & Packaging
- [ ] Automated tests
- [ ] Integration tests
- [ ] Acceptance criteria validation
- [ ] Windows installer
- [ ] Cross-platform bundles

## 🤝 Contributing

This is an MVP project built incrementally through PRs. Each PR focuses on a specific feature:

1. **scaffold** - Repository structure, hotkey, tray, IPC ← **You are here**
2. **stt** - Speech-to-text integration
3. **llm-planner** - LLM integration and planning
4. **executor** - Task execution engine
5. **packaging** - Distribution bundles

## 📄 License

MIT License - see LICENSE file for details

## 🔒 Security & Privacy

- **All processing is local**: No data leaves your machine
- **No telemetry**: No tracking or analytics
- **Whitelisted operations**: Only safe, approved operations can be executed
- **Audit logs**: All commands and actions are logged locally

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the PRD.md for detailed requirements
- Review the commit history for implementation details

---

**Status**: 🟡 MVP Development (Scaffold Phase)

**Next Steps**:
1. Test the scaffold on your development machine
2. Verify hotkey registration works
3. Confirm tray icon appears
4. Check Python backend starts (optional for scaffold)
5. Proceed to STT integration PR
