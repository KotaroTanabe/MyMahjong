import subprocess


def run_node(code: str) -> str:
    result = subprocess.run(
        ["node", "-e", code], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_draw_tile_flag_reduces_dead_wall() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {players:[{hand:{tiles:[],melds:[]},river:[]}], wall:{tiles:[{suit:'sou',value:9}]}, dead_wall:[{suit:'man',value:1}], current_player:0};\n"
        "const evt = {name:'draw_tile', payload:{player_index:0, tile:{suit:'sou',value:9}, replacement_for_kan:true}};\n"
        "const next = applyEvent(state, evt);\n"
        "console.log(next.dead_wall.length + ':' + next.wall.tiles.length + ':' + next.players[0].hand.tiles.length);"
    )
    output = run_node(code)
    assert output == '0:1:1'
