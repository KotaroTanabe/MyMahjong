from pathlib import Path


def test_tile_size_and_border() -> None:
    css = Path('web_gui/style.css').read_text()
    start = css.index('.tile {')
    end = css.index('}', start)
    tile_block = css[start:end]
    assert 'width: calc(var(--tile-font-size) * 1.2);' in tile_block
    assert 'height: calc(var(--tile-font-size) * 1.6);' in tile_block
    assert 'border: none;' in tile_block
    assert '1px solid' not in tile_block
