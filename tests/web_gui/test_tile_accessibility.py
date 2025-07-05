from pathlib import Path


def test_hand_has_aria_label() -> None:
    text = Path('web_gui/Hand.jsx').read_text()
    assert 'aria-label={`Discard' in text


def test_tile_transition_defined() -> None:
    css = Path('web_gui/style.css').read_text()
    assert 'transition: transform' in css
