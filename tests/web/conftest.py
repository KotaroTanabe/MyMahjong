import pytest
from web.server import manager
from core import api


@pytest.fixture(autouse=True)
def _reset_manager() -> None:
    manager._engines.clear()
    manager._next_id = 1
    api._engine = None  # type: ignore[assignment]
