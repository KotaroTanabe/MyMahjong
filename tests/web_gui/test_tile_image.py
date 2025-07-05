import subprocess


def run_node(code: str) -> str:
    result = subprocess.run([
        "node",
        "-e",
        code,
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_tile_to_image() -> None:
    output = run_node(
        "import { tileToImage } from './web_gui/tileUtils.js';\n"
        "console.log(tileToImage({suit: 'sou', value: 8}));"
    )
    assert output.endswith('sou_8.svg')
