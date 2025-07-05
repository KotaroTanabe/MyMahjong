import subprocess


def run_node(code: str) -> str:
    result = subprocess.run([
        "node",
        "-e",
        code,
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_draw_tile_removes_from_wall() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {players: [{hand: {tiles: []}, river: []}], \
wall: {tiles: [{suit: 'pin', value: 1}, {suit: 'pin', value: 2}]}};\n"
        "const evt = {name: 'draw_tile', payload: {player_index: 0, \
tile: {suit: 'pin', value: 1}}};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.wall.tiles.length);"
    )
    output = run_node(code)
    assert output == '1'
