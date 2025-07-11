import random
import pytest

@pytest.fixture(autouse=True)
def _seed_random() -> None:
    random.seed(0)


@pytest.fixture(autouse=True)
def _reset_manager() -> None:
    from core import api

    api.manager.reset()
    api._engine = None
