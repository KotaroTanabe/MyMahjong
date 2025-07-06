from pathlib import Path


def test_practice_uses_sort_tiles() -> None:
    text = Path('web_gui/Practice.jsx').read_text()
    assert 'sortTilesExceptLast' in text


def test_quiz_uses_sort_tiles() -> None:
    text = Path('web_gui/ShantenQuiz.jsx').read_text()
    assert 'sortTiles' in text


def test_app_passes_sort_prop() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert 'Practice server={server} sortHand={sortHand}' in text
    assert 'ShantenQuiz server={server} sortHand={sortHand}' in text
