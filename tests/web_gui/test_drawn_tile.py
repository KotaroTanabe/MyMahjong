from pathlib import Path
import subprocess


def run_node(code: str) -> str:
    result = subprocess.run(
        ["node", "-e", code], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_drawn_tile_css() -> None:
    css = Path('web_gui/style.css').read_text()
    assert '.drawn-tile' in css
    start = css.index('.drawn-tile')
    block = css[start:css.index('}', start)]
    assert 'margin-left:' in block


def test_sort_tiles_except_last() -> None:
    output = run_node(
        "import { sortTilesExceptLast } from './web_gui/tileUtils.js';\n"
        "const tiles = [\n"
        "  {suit: 'sou', value: 3},\n"
        "  {suit: 'man', value: 2},\n"
        "  {suit: 'pin', value: 1},\n"
        "  {suit: 'sou', value: 5}\n"
        "];\n"
        "const res = sortTilesExceptLast(tiles);\n"
        "console.log(JSON.stringify(res));"
    )
    assert output == (
        '[{"suit":"man","value":2},' +
        '{"suit":"pin","value":1},' +
        '{"suit":"sou","value":3},' +
        '{"suit":"sou","value":5}]'
    )


def test_hand_marks_last_tile() -> None:
    text = Path('web_gui/Hand.jsx').read_text()
    assert 'drawn-tile' in text
