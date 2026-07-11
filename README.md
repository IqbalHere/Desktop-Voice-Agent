<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:6C63FF,50:A855F7,100:EC4899&height=220&section=header&text=Desktop%20Voice%20Agent&fontSize=50&fontColor=FFFFFF&fontAlignY=35&desc=Local-first%20desktop%20voice%20automation&descSize=20&descAlignY=55&animation=fadeIn" width="100%" />
</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tauri](https://img.shields.io/badge/Tauri-Desktop%20UI-24C8D8?style=for-the-badge&logo=tauri&logoColor=white)
![Whisper](https://img.shields.io/badge/whisper.cpp-Local%20STT-6366F1?style=for-the-badge&logo=openai&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-111111?style=for-the-badge&logo=ollama&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Browser%20Automation-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Local%20Memory-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-TBD-lightgrey?style=for-the-badge)

</div>

<p align="center"><strong>An offline-first desktop agent that listens on hotkey, plans with a local LLM, and executes safe background actions.</strong></p>

<div align="center">
  🚀 <a href="#-quick-start">Quick Start</a> • 📖 <a href="#-development">Docs</a> • 🔧 <a href="#-configuration">Config</a> • 🤝 <a href="#-contributing">Contributing</a>
</div>

## ✨ Why Desktop Voice Agent?

|   | Feature |
|---|---|
| 🎙️ | **Hotkey Voice Activation** — Trigger listening with a configurable shortcut and capture voice commands quickly. |
| 🧠 | **Local LLM Planner** — Convert transcripts into structured JSON execution plans with confidence gating. |
| 🧰 | **Safe Tool Executor** — Run only whitelisted operations like app launch, command run, file write, browser open, and notifications. |
| 🔔 | **Background UX + Notifications** — Execute tasks asynchronously and notify success/failure without blocking desktop workflow. |
| 🛡️ | **Privacy + Safety by Default** — Keep audio/transcripts local and block dangerous operations unless explicitly elevated. |

## 🏗️ Architecture

```mermaid
graph LR
    A[⌨️ Hotkey Trigger] --> B[🎤 Local Audio Capture]
    B --> C[📝 STT Engine<br/>whisper.cpp / Vosk]
    C --> D[🧠 Local Planner LLM]
    D --> E[🧰 Whitelisted Executor]
    E --> F[🖥️ Desktop Actions]
    E --> G[🔔 Notifications + Logs]

    style A fill:#6C63FF,color:#fff,stroke:#4C1D95
    style B fill:#A855F7,color:#fff,stroke:#6B21A8
    style C fill:#F59E0B,color:#111,stroke:#B45309
    style D fill:#10B981,color:#fff,stroke:#047857
    style E fill:#EF4444,color:#fff,stroke:#991B1B
    style F fill:#6C63FF,color:#fff,stroke:#4C1D95
    style G fill:#A855F7,color:#fff,stroke:#6B21A8
```

## 📦 Prerequisites

| Requirement | Badge | Notes |
|---|---|---|
| Python | ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white) | Backend orchestrator target |
| Node.js | ![Node.js](https://img.shields.io/badge/Node.js-Required-339933?style=for-the-badge&logo=nodedotjs&logoColor=white) | Needed for Tauri frontend workflow |
| Rust | ![Rust](https://img.shields.io/badge/Rust-Required-000000?style=for-the-badge&logo=rust&logoColor=white) | Required by Tauri builds |
| STT Model Runtime | ![whisper.cpp](https://img.shields.io/badge/whisper.cpp-Local%20STT-6366F1?style=for-the-badge) | Local transcription |
| Local LLM Runtime | ![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-111111?style=for-the-badge&logo=ollama&logoColor=white) | Planner inference |

## 🚀 Quick Start

> [!IMPORTANT]
> This repository currently contains the product requirements (`PRD.md`) and implementation roadmap; code scaffold is planned next.

### 1️⃣ Clone repository
```bash
git clone https://github.com/IqbalHere/Desktop-Voice-Agent.git
cd Desktop-Voice-Agent
```

### 2️⃣ Review current scope
```bash
cat PRD.md
```

### 3️⃣ Start implementation from roadmap
```bash
# Begin with roadmap item #1 in PRD:
# "Create repository scaffold: Tauri tray + hotkey + Python IPC"
```

<details>
<summary>macOS/Linux notes</summary>

```bash
# Use your package manager to install python3, node, and rust toolchain
```

</details>

<details>
<summary>Windows notes</summary>

```powershell
# Install Python 3.11+, Node.js LTS, and Rust (rustup) before scaffolding
```

</details>

## 🔧 Configuration

| Variable | Required | Description |
|---|---|---|
| `HOTKEY` | ✅ | Keyboard shortcut that toggles microphone listening (example: `Ctrl+Space`). |
| `AUTO_CONFIRM_THRESHOLD` | ✅ | Confidence threshold for auto-run (recommended `> 0.85`). |
| `DEVELOPER_MODE` | ❌ | Enables elevated/risky operations for development use only. |
| `LOCAL_STT_MODEL` | ✅ | Path/model selection for local STT runtime (whisper.cpp or Vosk). |
| `LOCAL_LLM_MODEL` | ✅ | Local planner model selection (GGUF/Ollama-served model). |
| `LOG_RETENTION_DAYS` | ❌ | Log persistence duration before purge. |

> [!NOTE]
> Per PRD, all audio, transcript, and planning context should remain local by default, with explicit controls for purge and elevated execution.

## 📚 API / Tool Reference

### Planner output contract

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `plan` | `array<object>` | ✅ | `[]` | Ordered executable steps returned by planner. |
| `plan[].id` | `string` | ✅ | — | Step identifier (e.g., `s1`). |
| `plan[].type` | `string` | ✅ | — | Whitelisted tool type (`open_app`, `run_cmd`, etc.). |
| `plan[].args` | `object` | ✅ | `{}` | Tool arguments. |
| `plan[].explain` | `string` | ✅ | — | Human-readable step explanation. |
| `auto_confirm` | `boolean` | ✅ | `false` | Whether execution can run automatically. |
| `confidence` | `number` | ✅ | `0.0` | Planner confidence score. |

```json
{
  "plan": [
    {
      "id": "s1",
      "type": "open_app",
      "args": { "name": "chrome" },
      "explain": "Open Chrome"
    }
  ],
  "auto_confirm": true,
  "confidence": 0.91
}
```

## 🛡️ Error Handling

| Scenario | Behavior |
|---|---|
| 🚫 Non-whitelisted tool step | Reject step and notify user that action is blocked. |
| ❌ Dangerous command pattern detected | Prevent execution unless explicit elevated mode policy allows it. |
| 🔁 Step execution failure | Mark step `failed`, continue/stop by policy, and record logs with reason. |
| ↩️ Undo requested for reversible step | Attempt rollback (e.g., delete created file) or explain why rollback is unavailable. |

## 🧰 Development

### Dev workflow commands
```bash
# Current repo state: PRD-only (no runnable code scaffold yet)
cat PRD.md
```

### Project structure
```text
📦 Desktop-Voice-Agent
├── 📄 README.md
└── 📄 PRD.md
```

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Role |
|---|---|---|
| Desktop UI | ![Tauri](https://img.shields.io/badge/Tauri-24C8D8?style=for-the-badge&logo=tauri&logoColor=white) | Tray, global hotkey, overlay UI |
| Orchestrator | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | Command orchestration and execution flow |
| Speech-to-Text | ![whisper.cpp](https://img.shields.io/badge/whisper.cpp-6366F1?style=for-the-badge) | Local transcription |
| Planner LLM | ![Ollama](https://img.shields.io/badge/Ollama-111111?style=for-the-badge&logo=ollama&logoColor=white) | Local reasoning and plan generation |
| Automation | ![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white) | Browser automation in executor tools |
| Memory | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white) | Local logs and future memory storage |

</div>

## 🤝 Contributing

1. Fork this repository
2. Create a branch (`git checkout -b feature/your-change`)
3. Commit your changes (`git commit -m "feat: describe change"`)
4. Push your branch (`git push origin feature/your-change`)
5. Open a Pull Request

## 📄 License

License is currently **TBD**. Add a [`LICENSE`](./LICENSE) file to define distribution terms.

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:6C63FF,50:A855F7,100:EC4899&height=120&section=footer" width="100%" />
  <p><strong>Built with ❤️ by <a href="https://github.com/IqbalHere">Iqbal</a></strong></p>
  <p>
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/IqbalHere/Desktop-Voice-Agent?style=social" />
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/IqbalHere/Desktop-Voice-Agent?style=social" />
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/IqbalHere/Desktop-Voice-Agent?style=social" />
  </p>
  <p>⭐ Star this repo if you found it useful! ⭐</p>
</div>
