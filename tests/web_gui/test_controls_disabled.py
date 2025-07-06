from pathlib import Path


def test_controls_accepts_disabled_props() -> None:
    text = Path('web_gui/Controls.jsx').read_text()
    assert 'activePlayer' in text
    assert 'aiActive' in text
    assert 'allowedActions' in text
