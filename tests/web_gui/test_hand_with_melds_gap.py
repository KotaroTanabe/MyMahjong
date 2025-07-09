from pathlib import Path


def test_hand_with_melds_has_gap() -> None:
    css = Path('web_gui/style.css').read_text()
    start = css.index('.hand-with-melds')
    block = css[start:css.index('}', start)]
    assert 'gap:' in block
