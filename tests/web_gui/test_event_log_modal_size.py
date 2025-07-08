from pathlib import Path


def test_event_log_modal_has_custom_class() -> None:
    text = Path('web_gui/EventLogModal.jsx').read_text()
    assert 'event-log-modal-content' in text


def test_event_log_modal_css() -> None:
    css = Path('web_gui/style.css').read_text()
    assert '.event-log-modal-content' in css
    assert '80vw' in css
    assert '80vh' in css
