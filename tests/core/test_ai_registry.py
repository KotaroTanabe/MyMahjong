from core import api
import pytest


def test_auto_play_unknown_ai():
    api.start_game(["A", "B", "C", "D"])
    with pytest.raises(ValueError):
        api.auto_play_turn(ai_type="nonexistent")
