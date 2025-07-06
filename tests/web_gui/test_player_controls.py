from pathlib import Path


def test_center_display_in_panel_layout() -> None:
    text = Path('web_gui/GameBoard.jsx').read_text()
    assert text.count('CenterDisplay') >= 2


def test_controls_accept_player_index() -> None:
    text = Path('web_gui/Controls.jsx').read_text()
    assert 'playerIndex' in text
    assert 'player_index: playerIndex' in text


def test_game_board_has_controls_for_all_players() -> None:
    text = Path('web_gui/GameBoard.jsx').read_text()
    assert text.count('<Controls') >= 4
