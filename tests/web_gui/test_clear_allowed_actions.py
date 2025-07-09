from pathlib import Path


def test_allowed_actions_cleared_on_tsumo() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert 'setAllowedActions([[], [], [], []])' in text
    idx = text.index('setAllowedActions([[], [], [], []])')
    snippet = text[max(0, idx - 100): idx + 100]
    assert 'tsumo' in snippet
    assert 'ron' in snippet
    assert 'ryukyoku' in snippet
