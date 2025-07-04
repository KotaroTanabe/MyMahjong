from pathlib import Path


def test_index_html_exists() -> None:
    index = Path('web_gui/index.html')
    assert index.is_file(), 'index.html missing'
    text = index.read_text()
    assert 'MyMahjong GUI' in text
    assert 'main.js' in text


def test_main_js_exists() -> None:
    script = Path('web_gui/main.js')
    assert script.is_file(), 'main.js missing'
