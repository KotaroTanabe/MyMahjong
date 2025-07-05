from pathlib import Path


def test_start_kyoku_event_resets_state() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert "case 'start_kyoku'" in text, 'start_kyoku event not handled'
    idx = text.index("case 'start_kyoku'")
    snippet = text[idx: idx + 120]
    assert 'return event.payload.state' in snippet
