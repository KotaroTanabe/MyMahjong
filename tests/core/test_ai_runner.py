from core.ai_runner import ExternalAI
import subprocess


def test_external_ai_start(monkeypatch) -> None:
    calls = []

    class DummyPopen:
        def __init__(self, args, stdin=None, stdout=None, text=False):
            calls.append(args)
            self.stdin = None
            self.stdout = None

        def terminate(self) -> None:
            pass

        def wait(self) -> None:
            pass

    monkeypatch.setattr(subprocess, "Popen", DummyPopen)
    ai = ExternalAI(executable="ai_engine", model_dir="/models", player_id=2)
    ai.start()
    assert calls == [["ai_engine", "2", "--model-dir", "/models"]]
    ai.stop()
