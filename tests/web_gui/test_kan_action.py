import subprocess


def run_node(code: str) -> str:
    result = subprocess.run([
        'node',
        '-e',
        code,
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_apply_kan_updates_board_and_log() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "import { formatEvent } from './web_gui/eventLog.js';\n"
        "const state = {last_discard:{suit:'man',value:1}, last_discard_player:1, current_player:1,\n"
        "  players:[{hand:{tiles:[{suit:'man',value:1},{suit:'man',value:1},{suit:'man',value:1}], melds:[]}, river:[]},\n"
        "           {hand:{tiles:[], melds:[]}, river:[{suit:'man',value:1}]}]};\n"
        "const evt = {name:'meld', payload:{player_index:0, meld:{tiles:[{suit:'man',value:1},{suit:'man',value:1},{suit:'man',value:1},{suit:'man',value:1}], type:'kan', called_index:0}}};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.players[1].river.length + ':' + newState.players[0].hand.melds.length + ':' + newState.current_player + ':' + newState.last_discard + ':' + formatEvent(evt));"
    )
    output = run_node(code)
    assert output == '0:1:0:null:Player 0 calls kan'
