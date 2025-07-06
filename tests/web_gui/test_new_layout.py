from pathlib import Path


def test_alt_layout_class_in_css() -> None:
    css = Path('web_gui/style.css').read_text()
    assert '.board-grid-alt' in css


def test_game_board_supports_layout_prop() -> None:
    jsx = Path('web_gui/GameBoard.jsx').read_text()
    assert 'layout ===' in jsx and 'board-grid-alt' in jsx
