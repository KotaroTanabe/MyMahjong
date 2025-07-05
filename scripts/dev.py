#!/usr/bin/env python3
"""Run the FastAPI backend and React front-end together."""

from __future__ import annotations

import signal
import subprocess
import sys
from typing import List

BACKEND_CMD = ["uvicorn", "web.server:app", "--reload"]
FRONTEND_CMD = ["npx", "vite", "--open"]


def start_processes() -> List[subprocess.Popen]:
    """Start backend and frontend processes and return them."""
    backend = subprocess.Popen(BACKEND_CMD)
    frontend = subprocess.Popen(FRONTEND_CMD, cwd="web_gui")
    return [backend, frontend]


def terminate_processes(processes: List[subprocess.Popen]) -> None:
    """Terminate all given processes."""
    for p in processes:
        if p.poll() is None:
            p.terminate()
    for p in processes:
        try:
            p.wait(timeout=5)
        except Exception:
            p.kill()


def main() -> None:
    processes = start_processes()

    def _handle(signum: int, frame: object) -> None:
        terminate_processes(processes)
        sys.exit(0)

    signal.signal(signal.SIGINT, _handle)
    signal.signal(signal.SIGTERM, _handle)

    try:
        processes[0].wait()
    finally:
        terminate_processes(processes)


if __name__ == "__main__":
    main()
