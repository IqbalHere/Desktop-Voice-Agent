// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{AppHandle, Manager};
use tauri::menu::{Menu, MenuItem};
use tauri::tray::TrayIconBuilder;
use tauri_plugin_global_shortcut::{ShortcutState, GlobalShortcutExt};
use tauri_plugin_notification::NotificationExt;
use std::sync::{Arc, Mutex};
use std::process::{Command, Child, Stdio};

// State to track the Python backend process
#[allow(dead_code)]
struct PythonBackend {
    process: Arc<Mutex<Option<Child>>>,
}

// Command to trigger voice capture
#[tauri::command]
fn trigger_voice_capture(app: AppHandle) -> Result<String, String> {
    println!("Voice capture triggered!");
    
    // Send notification using the notification plugin
    app.notification()
        .builder()
        .title("Voice Agent")
        .body("Listening... Press Ctrl+Space again to stop")
        .show()
        .map_err(|e| e.to_string())?;
    
    // In a real implementation, this would:
    // 1. Start audio recording
    // 2. Send audio to Python backend via IPC
    // 3. Get transcription back
    // 4. Send to LLM planner
    // 5. Execute plan
    
    Ok("Voice capture started".to_string())
}

// Command to send data to Python backend
#[tauri::command]
async fn send_to_backend(data: String) -> Result<String, String> {
    println!("Sending to backend: {}", data);
    
    // TODO: Implement actual IPC communication with Python backend
    // For now, this is a placeholder that returns a mock response
    
    Ok(format!("Backend received: {}", data))
}

// Command to get backend status
#[tauri::command]
fn get_backend_status() -> Result<String, String> {
    // TODO: Check if Python backend is running
    Ok("Backend status: Running".to_string())
}

// Command to show main window (for settings, etc.)
#[tauri::command]
fn show_main_window(app: AppHandle) -> Result<(), String> {
    if let Some(window) = app.get_webview_window("main") {
        window.show().map_err(|e| e.to_string())?;
        window.set_focus().map_err(|e| e.to_string())?;
    }
    Ok(())
}

fn start_python_backend(backend_state: Arc<Mutex<Option<Child>>>) -> Result<(), String> {
    println!("Starting Python backend...");
    
    // Start Python backend process
    // In production, this would use the packaged Python interpreter
    let child = Command::new("python3")
        .arg("-u") // Unbuffered output
        .arg("backend/main.py")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to start Python backend: {}", e))?;
    
    println!("Python backend started with PID: {:?}", child.id());
    
    // Store the process handle
    *backend_state.lock().unwrap() = Some(child);
    
    Ok(())
}

fn main() {
    // Create shared state for Python backend
    let backend_state = Arc::new(Mutex::new(None));
    let backend_state_clone = backend_state.clone();

    tauri::Builder::default()
        .plugin(tauri_plugin_global_shortcut::Builder::new().build())
        .plugin(tauri_plugin_notification::init())
        .plugin(tauri_plugin_shell::init())
        .manage(PythonBackend {
            process: backend_state.clone(),
        })
        .setup(move |app| {
            // Start Python backend
            if let Err(e) = start_python_backend(backend_state_clone) {
                eprintln!("Warning: Failed to start Python backend: {}", e);
                eprintln!("The application will continue, but backend features may not work.");
            }

            // Create tray menu
            let trigger_i = MenuItem::with_id(app, "trigger", "Trigger Voice Capture (Ctrl+Space)", true, None::<&str>).unwrap();
            let settings_i = MenuItem::with_id(app, "settings", "Settings", true, None::<&str>).unwrap();
            let logs_i = MenuItem::with_id(app, "logs", "View Logs", true, None::<&str>).unwrap();
            let quit_i = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>).unwrap();
            
            let menu = Menu::with_items(app, &[
                &trigger_i,
                &settings_i,
                &logs_i,
                &quit_i,
            ]).unwrap();

            // Create tray icon
            let _tray = TrayIconBuilder::new()
                .icon(app.default_window_icon().unwrap().clone())
                .menu(&menu)
                .on_menu_event(|app, event| {
                    match event.id.as_ref() {
                        "trigger" => {
                            let _ = trigger_voice_capture(app.clone());
                        }
                        "settings" => {
                            let _ = show_main_window(app.clone());
                        }
                        "logs" => {
                            println!("Opening logs...");
                        }
                        "quit" => {
                            std::process::exit(0);
                        }
                        _ => {}
                    }
                })
                .build(app)?;

            // Register global hotkey (Ctrl+Space)
            let app_handle = app.handle().clone();
            
            app.global_shortcut().on_shortcut("CommandOrControl+Space", move |_app, _shortcut, event| {
                if event.state == ShortcutState::Pressed {
                    let _ = trigger_voice_capture(app_handle.clone());
                }
            }).unwrap();

            // Register the hotkey
            app.global_shortcut()
                .register("CommandOrControl+Space")
                .expect("Failed to register global hotkey");

            println!("Desktop Voice Agent started!");
            println!("Press Ctrl+Space (or Cmd+Space on macOS) to trigger voice capture");

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            trigger_voice_capture,
            send_to_backend,
            get_backend_status,
            show_main_window
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
