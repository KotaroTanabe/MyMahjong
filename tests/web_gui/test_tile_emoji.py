import subprocess


def run_node(code: str) -> str:
    result = subprocess.run([
        "node",
        "-e",
        code,
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_tile_to_emoji() -> None:
    output = run_node(
        "import { tileToEmoji } from './web_gui/tileUtils.js';\n"
        "console.log(tileToEmoji({suit: 'sou', value: 8}));"
    )
    assert output == '🀗'
