from pathlib import Path


def test_uvicorn_standard_dependency() -> None:
    text = Path('web/pyproject.toml').read_text()
    assert 'uvicorn[standard]' in text
