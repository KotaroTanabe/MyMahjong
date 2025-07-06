from pathlib import Path


def test_active_player_css() -> None:
    css = Path('web_gui/style.css').read_text()
    block_start = css.index('.active-player')
    block = css[block_start:css.index('}', block_start)]
    assert 'font-weight: bold' in block


def test_game_board_passes_prop() -> None:
    jsx = Path('web_gui/GameBoard.jsx').read_text()
    assert 'activePlayer={active}' in jsx


def test_player_panel_accepts_prop() -> None:
    jsx = Path('web_gui/PlayerPanel.jsx').read_text()
    assert 'activePlayer' in jsx
    assert 'active-player' in jsx
    assert 'aiActive' in jsx
