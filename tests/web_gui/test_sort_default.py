from pathlib import Path


def test_sort_hand_default_on() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert 'useState(true)' in text and 'sortHand' in text

