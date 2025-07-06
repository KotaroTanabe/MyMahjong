from pathlib import Path


def test_hand_with_melds_row() -> None:
    css = Path('web_gui/style.css').read_text()
    start = css.index('.hand-with-melds')
    block = css[start:css.index('}', start)]
    assert 'flex-direction: row' in block
    jsx = Path('web_gui/PlayerPanel.jsx').read_text()
    hand_idx = jsx.find('<Hand')
    meld_idx = jsx.find('<MeldArea')
    assert hand_idx != -1 and meld_idx != -1
    assert hand_idx < meld_idx
