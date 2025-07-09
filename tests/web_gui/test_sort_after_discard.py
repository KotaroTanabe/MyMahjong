from pathlib import Path


def test_game_board_resorts_hand() -> None:
    text = Path('web_gui/GameBoard.jsx').read_text()
    start = text.index('const southHand')
    snippet = text[start:text.index(';', start)]
    assert 'hasDrawnTile(south, 0)' in snippet
    assert 'sortTilesExceptLast' in snippet
    assert 'sortTiles(southTiles)' in snippet
