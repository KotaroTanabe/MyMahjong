"""Run both FastAPI backend and React frontend for local development."""
from __future__ import annotations

import subprocess
import time
from pathlib import Path


BACKEND_CMD = ["uvicorn", "web.server:app", "--reload"]
FRONTEND_CMD = ["npx", "vite", "--open"]


def main() -> None:
    """Launch the backend and frontend concurrently."""
    frontend_cwd = Path(__file__).parent / "web_gui"
    backend = subprocess.Popen(BACKEND_CMD)
    frontend = subprocess.Popen(FRONTEND_CMD, cwd=frontend_cwd)
    try:
        while True:
            if backend.poll() is not None or frontend.poll() is not None:
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        frontend.terminate()
        backend.terminate()


if __name__ == "__main__":
    main()
