import subprocess


def run_node(code: str) -> str:
    result = subprocess.run([
        "node",
        "-e",
        code,
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_format_draw_tile() -> None:
    code = (
        "import { formatEvent } from './web_gui/eventLog.js';\n"
        "const evt = {name:'draw_tile', payload:{player_index:1, tile:{suit:'man', value:2}}};\n"
        "console.log(formatEvent(evt));"
    )
    assert run_node(code) == 'Player 1 draws 2 man'


def test_format_unknown_event() -> None:
    code = (
        "import { formatEvent } from './web_gui/eventLog.js';\n"
        "console.log(formatEvent({name:'foo'}));"
    )
    assert run_node(code) == 'foo'

