"""Wrapper for running an external MJAI-based AI engine as a subprocess."""
from __future__ import annotations

import subprocess
from typing import Optional


class ExternalAI:
    """Launch and communicate with an external AI via MJAI messages."""

    def __init__(
        self,
        executable: str = "ai_engine",
        model_dir: str = ".",
        player_id: int = 0,
    ) -> None:
        self.executable = executable
        self.model_dir = model_dir
        self.player_id = player_id
        self.process: Optional[subprocess.Popen[str]] = None

    def start(self) -> None:
        """Start the AI process if not already running."""
        if self.process is not None:
            return
        self.process = subprocess.Popen(
            [
                self.executable,
                str(self.player_id),
                "--model-dir",
                self.model_dir,
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )

    def send(self, message: str) -> None:
        """Send an MJAI event to the AI."""
        assert self.process is not None and self.process.stdin is not None
        self.process.stdin.write(message + "\n")
        self.process.stdin.flush()

    def receive(self) -> str:
        """Read a response from the AI."""
        assert self.process is not None and self.process.stdout is not None
        line = self.process.stdout.readline()
        return line.strip()

    def stop(self) -> None:
        """Terminate the AI process."""
        if self.process is not None:
            self.process.terminate()
            self.process.wait()
            self.process = None
