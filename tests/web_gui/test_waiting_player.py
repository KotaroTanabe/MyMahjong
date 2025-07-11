from pathlib import Path


def test_waiting_player_css() -> None:
    css = Path('web_gui/style.css').read_text()
    assert '.waiting-player' not in css


def test_player_panel_waiting_class() -> None:
    jsx = Path('web_gui/PlayerPanel.jsx').read_text()
    assert 'waiting-player' not in jsx
