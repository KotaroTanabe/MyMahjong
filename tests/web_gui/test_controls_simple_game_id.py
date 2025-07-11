from pathlib import Path


def test_controls_simple_uses_game_id() -> None:
    text = Path('web_gui/Controls.jsx').read_text()
    assert '/games/${gameId}/action' in text
    assert '/games/1/action' not in text
