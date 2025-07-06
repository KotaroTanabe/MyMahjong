from pathlib import Path


def test_controls_simple_uses_game_id() -> None:
    lines = Path('web_gui/Controls.jsx').read_text().splitlines()
    snippet = "\n".join(lines[8:16])
    assert '/games/${gameId}/action' in snippet
    assert '/games/1/action' not in snippet
