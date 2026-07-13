#!/usr/bin/env python3
"""
Desktop Voice Agent - Backend Main Entry Point

This module serves as the backend orchestrator for the Desktop Voice Agent.
It handles:
- IPC communication with the Tauri frontend
- Audio processing and STT coordination
- LLM planner integration
- Task execution

For the MVP scaffold, this provides a basic IPC server that can receive
commands from the frontend.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any
import time
import threading
import numpy as np

try:
    import whisper
    import sounddevice as sd
    import soundfile as sf
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("Warning: whisper or sounddevice not installed. STT will be mocked.", file=sys.stderr)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('backend.log')
    ]
)

logger = logging.getLogger(__name__)


class VoiceAgentBackend:
    """Main backend orchestrator for the voice agent."""

    def __init__(self):
        """Initialize the backend."""
        self.running = False
        self.is_recording = False
        self.audio_data = []
        self.audio_stream = None
        self.sample_rate = 16000

        logger.info("Desktop Voice Agent Backend initializing...")
        if WHISPER_AVAILABLE:
            logger.info("Loading Whisper model (base)...")
            self.whisper_model = whisper.load_model("base")
        else:
            self.whisper_model = None

    def start(self):
        """Start the backend service."""
        self.running = True
        logger.info("Backend started successfully!")
        logger.info("Waiting for commands from frontend...")

        # Keep the process alive
        try:
            while self.running:
                # Read from stdin (IPC from Tauri)
                line = sys.stdin.readline()
                if not line:
                    # EOF reached, parent process closed
                    logger.info("EOF reached on stdin, shutting down backend...")
                    break

                self.process_command(line.strip())
                time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        finally:
            self.shutdown()

    def process_command(self, command_str: str):
        """
        Process a command received from the frontend.

        Args:
            command_str: JSON string containing the command
        """
        try:
            command = json.loads(command_str)
            logger.info(f"Received command: {command}")

            # Process different command types
            cmd_type = command.get('type', 'unknown')

            if cmd_type == 'start_recording':
                self.handle_start_recording(command)
            elif cmd_type == 'stop_recording_and_transcribe':
                self.handle_stop_recording_and_transcribe(command)
            elif cmd_type == 'transcribe':
                self.handle_transcribe(command)
            elif cmd_type == 'plan':
                self.handle_plan(command)
            elif cmd_type == 'execute':
                self.handle_execute(command)
            elif cmd_type == 'status':
                self.handle_status(command)
            else:
                logger.warning(f"Unknown command type: {cmd_type}")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse command JSON: {e}")
        except Exception as e:
            logger.error(f"Error processing command: {e}", exc_info=True)

    def audio_callback(self, indata, frames, time_info, status):
        """Callback for sounddevice to capture audio chunks."""
        if status:
            logger.warning(f"Audio status: {status}")
        if self.is_recording:
            self.audio_data.append(indata.copy())

    def handle_start_recording(self, command: Dict[str, Any]):
        """Start recording audio from microphone."""
        if not WHISPER_AVAILABLE:
            logger.warning("Whisper/sounddevice not available, cannot start recording.")
            self.send_response({"type": "recording_started", "status": "mock"})
            return

        logger.info("Starting audio recording...")
        self.is_recording = True
        self.audio_data = []
        try:
            self.audio_stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32',
                callback=self.audio_callback
            )
            self.audio_stream.start()
            self.send_response({"type": "recording_started", "status": "ok"})
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            self.is_recording = False
            self.send_response({"type": "error", "message": f"Failed to start recording: {e}"})

    def handle_stop_recording_and_transcribe(self, command: Dict[str, Any]):
        """Stop recording and transcribe the captured audio."""
        logger.info("Stopping recording and transcribing...")

        audio_path = command.get("audio_path")
        if audio_path:
            # Used for testing/headless environments
            self.is_recording = False
            if self.audio_stream:
                self.audio_stream.stop()
                self.audio_stream.close()
                self.audio_stream = None
            return self.transcribe_file(audio_path)

        if not WHISPER_AVAILABLE:
            self.send_response({
                'type': 'transcribe_result',
                'text': 'Mock transcription result (dependencies missing)',
                'confidence': 0.95
            })
            return

        self.is_recording = False
        if self.audio_stream:
            self.audio_stream.stop()
            self.audio_stream.close()
            self.audio_stream = None

        if not self.audio_data:
            logger.warning("No audio data captured.")
            self.send_response({"type": "error", "message": "No audio captured"})
            return

        # Concatenate audio chunks
        audio_np = np.concatenate(self.audio_data, axis=0).flatten()

        # Transcribe directly from numpy array (whisper accepts float32 numpy arrays)
        try:
            logger.info("Transcribing captured audio...")
            result = self.whisper_model.transcribe(audio_np, fp16=False)
            text = result.get("text", "").strip()

            # Since whisper doesn't give simple confidence scores by default for the whole string,
            # we'll mock the confidence for now based on segments if needed, or default to 0.95.
            response = {
                'type': 'transcribe_result',
                'text': text,
                'confidence': 0.95
            }
            self.send_response(response)
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            self.send_response({"type": "error", "message": str(e)})

    def transcribe_file(self, audio_path: str):
        if not WHISPER_AVAILABLE:
            self.send_response({
                'type': 'transcribe_result',
                'text': 'Mock transcription result (dependencies missing)',
                'confidence': 0.95
            })
            return

        try:
            logger.info(f"Transcribing file: {audio_path}")
            result = self.whisper_model.transcribe(audio_path, fp16=False)
            text = result.get("text", "").strip()
            response = {
                'type': 'transcribe_result',
                'text': text,
                'confidence': 0.95
            }
            self.send_response(response)
        except Exception as e:
            logger.error(f"Transcription failed for file {audio_path}: {e}")
            self.send_response({"type": "error", "message": str(e)})

    def handle_transcribe(self, command: Dict[str, Any]):
        """Legacy Handle audio transcription request."""
        logger.info("Legacy Transcription requested")
        self.send_response({
            'type': 'transcribe_result',
            'text': 'Mock transcription result',
            'confidence': 0.95
        })

    def handle_plan(self, command: Dict[str, Any]):
        """Handle planning request using local LLM."""
        logger.info("Planning requested")
        # TODO: Implement LLM planner
        response = {
            'type': 'plan_result',
            'plan': [
                {
                    'id': 's1',
                    'type': 'notify',
                    'args': {'message': 'Mock plan step'},
                    'explain': 'This is a mock plan step'
                }
            ],
            'auto_confirm': True,
            'confidence': 0.90
        }
        self.send_response(response)

    def handle_execute(self, command: Dict[str, Any]):
        """Handle plan execution request."""
        logger.info("Execution requested")
        # TODO: Implement executor
        response = {
            'type': 'execute_result',
            'status': 'ok',
            'results': []
        }
        self.send_response(response)

    def handle_status(self, command: Dict[str, Any]):
        """Handle status check request."""
        response = {
            'type': 'status_result',
            'running': self.running,
            'version': '0.1.0'
        }
        self.send_response(response)

    def send_response(self, response: Dict[str, Any]):
        """
        Send a response back to the frontend via stdout.

        Args:
            response: Response dictionary to send
        """
        try:
            response_str = json.dumps(response)
            print(response_str, flush=True)
            logger.debug(f"Sent response: {response_str}")
        except Exception as e:
            logger.error(f"Failed to send response: {e}")

    def shutdown(self):
        """Shutdown the backend gracefully."""
        logger.info("Shutting down backend...")
        self.running = False


def main():
    """Main entry point."""
    logger.info("=" * 60)
    logger.info("Desktop Voice Agent Backend - MVP Scaffold")
    logger.info("=" * 60)

    backend = VoiceAgentBackend()
    backend.start()


if __name__ == '__main__':
    main()
