import random
import pytest

@pytest.fixture(autouse=True)
def _seed_random() -> None:
    random.seed(0)
