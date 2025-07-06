from pathlib import Path


def test_game_board_passes_actions() -> None:
    text = Path('web_gui/GameBoard.jsx').read_text()
    assert 'availableActions(state, 0)' in text
