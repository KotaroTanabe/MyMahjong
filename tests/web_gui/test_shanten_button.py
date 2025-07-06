from pathlib import Path


def test_controls_has_shanten_button() -> None:
    text = Path('web_gui/Controls.jsx').read_text()
    assert 'Shanten' in text
    assert '/games/${gameId}/shanten' in text
