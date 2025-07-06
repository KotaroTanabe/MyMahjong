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


def test_skip_updates_current_player() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {current_player: 0, players: [{}, {}]};\n"
        "const evt = {name: 'skip', payload: {player_index: 0}};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.current_player);"
    )
    output = run_node(code)
    assert output == '1'


def test_discard_advances_turn_and_adds_river() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {current_player: 0, players: [\n"
        "  {hand: {tiles: [{suit: 'pin', value: 1}]}, river: []}, {}\n"
        "]};\n"
        "const evt = {name: 'discard', payload: {player_index: 0, tile: {suit: 'pin', value: 1}}};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.current_player + ':' + newState.players[0].river.length);"
    )
    output = run_node(code)
    assert output == '1:1'


def test_discard_sets_waiting_for_claims() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {current_player:0, players:[{hand:{tiles:[]},river:[]},{hand:{tiles:[]},river:[]},{hand:{tiles:[]},river:[]},{hand:{tiles:[]},river:[]}]};\n"
        "const evt = {name:'discard', payload:{player_index:0, tile:{suit:'pin', value:1}}};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.waiting_for_claims.length + ':' + newState.waiting_for_claims.includes(1));"
    )
    output = run_node(code)
    assert output == '3:true'

def test_ryukyoku_sets_result_and_scores() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {players: [{score:25000},{score:25000},{score:25000},{score:25000}]};\n"
        "const evt = {name:'ryukyoku', payload:{reason:'wall_empty', tenpai:[true,false,true,false], scores:[26500,23500,26500,23500]}};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.result.type + ':' + newState.players[0].score);"
    )
    output = run_node(code)
    assert output == 'ryukyoku:26500'


def test_riichi_event_updates_score_and_sticks() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {players:[{score:25000,riichi:false}],riichi_sticks:0};\n"
        "const evt = {name:'riichi', payload:{player_index:0, score:24000, riichi_sticks:1}};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.players[0].score + ':' + newState.riichi_sticks + ':' + newState.players[0].riichi);"
    )
    output = run_node(code)
    assert output == '24000:1:true'
