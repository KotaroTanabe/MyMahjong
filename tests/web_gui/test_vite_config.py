from pathlib import Path


def test_vite_base_path() -> None:
    config = Path('web_gui/vite.config.js').read_text()
    assert "base: '/MyMahjong/'" in config, 'Vite base path not set'
