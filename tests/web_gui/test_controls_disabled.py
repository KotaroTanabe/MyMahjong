from pathlib import Path


def test_controls_buttons_have_disabled_props() -> None:
    text = Path('web_gui/Controls.jsx').read_text()
    assert 'disabled={!canChi}' in text
    assert 'disabled={!canPon}' in text
    assert 'disabled={!canKan}' in text
