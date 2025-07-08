from pathlib import Path


def test_waiting_player_css() -> None:
    css = Path('web_gui/style.css').read_text()
    assert '.waiting-player' in css
    start = css.index('.waiting-player')
    block = css[start:css.index('}', start)]
    assert 'background-color' in block
    assert '#fff4ce' not in block


def test_player_panel_waiting_class() -> None:
    jsx = Path('web_gui/PlayerPanel.jsx').read_text()
    assert 'waiting-player' in jsx
