from pathlib import Path


def test_button_component_exists() -> None:
    btn = Path('web_gui/Button.jsx')
    assert btn.is_file(), 'Button.jsx missing'
    text = btn.read_text()
    assert 'flat-btn' in text
