from pathlib import Path


def test_center_display_supports_status_message() -> None:
    jsx = Path('web_gui/CenterDisplay.jsx').read_text()
    assert 'statusMessage' in jsx
    assert 'turn-status' in jsx


def test_game_board_passes_status_message() -> None:
    jsx = Path('web_gui/GameBoard.jsx').read_text()
    assert 'statusMessage={statusMessage}' in jsx
    assert 'const active' in jsx
