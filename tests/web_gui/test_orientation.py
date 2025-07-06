from pathlib import Path


def test_grid_orientation() -> None:
    css = Path('web_gui/style.css').read_text()
    assert 'north center east' in css
    assert 'west center south' in css


def test_dom_order() -> None:
    jsx = Path('web_gui/GameBoard.jsx').read_text()
    north_idx = jsx.find('seat="north"')
    east_idx = jsx.find('seat="east"')
    center_idx = jsx.find('className="center"')
    west_idx = jsx.find('seat="west"')
    south_idx = jsx.find('seat="south"')
    assert -1 not in (north_idx, east_idx, center_idx, west_idx, south_idx)
    assert north_idx < east_idx < center_idx < west_idx < south_idx
