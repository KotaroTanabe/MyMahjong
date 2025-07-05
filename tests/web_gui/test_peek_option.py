from pathlib import Path


def test_app_has_peek_toggle() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert 'Peek' in text
    assert 'setPeek' in text


def test_game_board_accepts_peek_prop() -> None:
    text = Path('web_gui/GameBoard.jsx').read_text()
    assert 'peek =' in text or 'peek=' in text
