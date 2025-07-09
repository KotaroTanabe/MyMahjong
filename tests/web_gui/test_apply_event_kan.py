import subprocess


def run_node(code: str) -> str:
    result = subprocess.run([
        "node",
        "-e",
        code,
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_draw_tile_after_kan_does_not_pop_wall() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {\n"
        "  players: [{hand:{tiles:[\n"
        "    {suit:'man',value:5},\n"
        "    {suit:'man',value:5},\n"
        "    {suit:'man',value:5},\n"
        "    {suit:'man',value:5}\n"
        "  ],melds:[]},river:[]}],\n"
        "  wall:{tiles:[{suit:'pin',value:1}]},\n"
        "  current_player:0\n"
        "};\n"
        "const meldEvt = {name:'meld', payload:{player_index:0, meld:{tiles:[{suit:'man',value:5},{suit:'man',value:5},{suit:'man',value:5},{suit:'man',value:5}], type:'closed_kan'}}};\n"
        "let next = applyEvent(state, meldEvt);\n"
        "const drawEvt = {name:'draw_tile', payload:{player_index:0, tile:{suit:'pin',value:1}, from_dead_wall:true}};\n"
        "next = applyEvent(next, drawEvt);\n"
        "console.log(next.wall.tiles.length + ':' + next.players[0].hand.tiles.length);"
    )
    output = run_node(code)
    assert output == '1:1'

