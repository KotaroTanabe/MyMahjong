from pathlib import Path


def test_ai_button_added() -> None:
    jsx = Path('web_gui/PlayerPanel.jsx').read_text()
    assert 'ai-btn' in jsx and 'FiCpu' in jsx


def test_ai_button_css() -> None:
    css = Path('web_gui/style.css').read_text()
    assert '.ai-btn' in css
