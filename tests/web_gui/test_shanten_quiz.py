from pathlib import Path


def test_shanten_quiz_component_exists() -> None:
    comp = Path('web_gui/ShantenQuiz.jsx')
    assert comp.is_file(), 'ShantenQuiz.jsx missing'


def test_app_has_shanten_mode() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert 'Shanten Quiz' in text
    assert 'ShantenQuiz' in text
