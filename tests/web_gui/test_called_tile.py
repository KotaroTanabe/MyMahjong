from pathlib import Path


def test_called_tile_css_present() -> None:
    css = Path('web_gui/style.css').read_text()
    assert '.called-tile' in css
    start = css.index('.called-tile')
    block = css[start:css.index('}', start)]
    assert 'rotate(90deg)' in block


def test_meld_area_not_rotated() -> None:
    css = Path('web_gui/style.css').read_text()
    assert 'east .meld-area' not in css
    assert 'north .meld-area' not in css
    assert 'west .meld-area' not in css
