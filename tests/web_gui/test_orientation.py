from pathlib import Path


def test_grid_orientation() -> None:
    css = Path('web_gui/style.css').read_text()
    assert "'north west'" in css or 'north west' in css
    assert "'east south'" in css or 'east south' in css


def test_dom_order() -> None:
    jsx = Path('web_gui/GameBoard.jsx').read_text()
    north_idx = jsx.find('seat="north"')
    east_idx = jsx.find('seat="east"')
    west_idx = jsx.find('seat="west"')
    south_idx = jsx.find('seat="south"')
    center_idx = jsx.find('CenterDisplay')
    assert -1 not in (north_idx, east_idx, west_idx, south_idx, center_idx)
    assert center_idx < north_idx < west_idx < east_idx < south_idx
