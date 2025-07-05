import subprocess
from pathlib import Path

import run_local


def test_run_local_starts_processes(monkeypatch):
    calls = []

    class DummyPopen:
        def __init__(self, cmd, cwd=None):
            calls.append((cmd, cwd))
            self._count = 0

        def poll(self):
            self._count += 1
            return 0 if self._count > 1 else None

        def terminate(self):
            pass

    monkeypatch.setattr(subprocess, "Popen", DummyPopen)
    monkeypatch.setattr(run_local, "time", type("t", (), {"sleep": lambda self, _: None})())
    run_local.main()

    assert calls[0][0] == run_local.BACKEND_CMD
    assert calls[1][0] == run_local.FRONTEND_CMD
    assert Path(calls[1][1]).name == "web_gui"
