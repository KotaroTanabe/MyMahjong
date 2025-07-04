from core.mortal_runner import MortalAI
import subprocess


def test_mortal_ai_start(monkeypatch) -> None:
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
    ai = MortalAI(executable="mortal", model_dir="/models", player_id=2)
    ai.start()
    assert calls == [["mortal", "2", "--model-dir", "/models"]]
    ai.stop()
