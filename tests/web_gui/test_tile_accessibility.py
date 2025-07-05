from pathlib import Path


def test_tile_image_asset_exists() -> None:
    path = Path('web_gui/assets/sou_1.svg')
    assert path.is_file(), 'sou_1.svg missing'


def test_hand_uses_img_tags() -> None:
    text = Path('web_gui/Hand.jsx').read_text()
    assert '<img' in text, 'Hand component should use img tags'


def test_tile_button_has_aria_label() -> None:
    text = Path('web_gui/Hand.jsx').read_text()
    assert 'aria-label={`Discard' in text


def test_tile_transition_defined() -> None:
    css = Path('web_gui/style.css').read_text()
    assert 'transition: transform' in css
