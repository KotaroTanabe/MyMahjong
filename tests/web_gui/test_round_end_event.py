from pathlib import Path


def test_round_end_event_handled() -> None:
    text = Path('web_gui/applyEvent.js').read_text()
    assert "case 'round_end'" in text
