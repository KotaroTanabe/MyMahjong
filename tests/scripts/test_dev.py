from scripts import dev
import subprocess

class DummyProcess:
    def __init__(self, cmd, cwd=None):
        self.cmd = cmd
        self.cwd = cwd
    def poll(self):
        return 0
    def terminate(self):
        self.terminated = True
    def wait(self, timeout=None):
        return 0

def test_start_processes(monkeypatch):
    calls = []
    def fake_popen(cmd, cwd=None):
        p = DummyProcess(cmd, cwd)
        calls.append((cmd, cwd))
        return p
    monkeypatch.setattr(subprocess, 'Popen', fake_popen)
    procs = dev.start_processes()
    assert calls[0] == (dev.BACKEND_CMD, None)
    assert calls[1] == (dev.FRONTEND_CMD, 'web_gui')
    assert len(procs) == 2
