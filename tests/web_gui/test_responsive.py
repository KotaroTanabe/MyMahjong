from pathlib import Path


def test_style_contains_media_query() -> None:
    css = Path('web_gui/style.css').read_text()
    assert '@media (max-width' in css
