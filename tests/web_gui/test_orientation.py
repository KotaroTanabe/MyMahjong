from pathlib import Path


def test_grid_orientation() -> None:
    css = Path('web_gui/style.css').read_text()
    assert 'east center west' in css


def test_dom_order() -> None:
    jsx = Path('web_gui/GameBoard.jsx').read_text()
    east_idx = jsx.find('className="east seat"')
    west_idx = jsx.find('className="west seat"')
    assert -1 not in (east_idx, west_idx)
    assert east_idx < west_idx
