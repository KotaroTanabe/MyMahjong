from pathlib import Path


def test_index_html_exists() -> None:
    index = Path('web_gui/index.html')
    assert index.is_file(), 'index.html missing'
    text = index.read_text()
    assert 'MyMahjong GUI' in text
    assert '<div id="app"></div>' in text
    assert 'main.jsx' in text


def test_main_js_exists() -> None:
    script = Path('web_gui/main.jsx')
    assert script.is_file(), 'main.jsx missing'


def test_app_jsx_exists() -> None:
    app = Path('web_gui/App.jsx')
    assert app.is_file(), 'App.jsx missing'
