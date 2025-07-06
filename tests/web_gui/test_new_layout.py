from pathlib import Path


def test_player_panel_layout_css() -> None:
    css = Path('web_gui/style.css').read_text()
    assert '.board-grid' in css


def test_game_board_uses_player_panels() -> None:
    jsx = Path('web_gui/GameBoard.jsx').read_text()
    assert 'PlayerPanel' in jsx
