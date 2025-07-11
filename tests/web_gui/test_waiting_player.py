from pathlib import Path


def test_waiting_discard_css() -> None:
    css = Path('web_gui/style.css').read_text()
    assert '.waiting-discard' in css
    start = css.index('.waiting-discard')
    block = css[start:css.index('}', start)]
    assert 'box-shadow' in block


def test_waiting_discard_usage() -> None:
    jsx = Path('web_gui/River.jsx').read_text()
    assert 'waiting-discard' in jsx
