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


def test_replacement_draw_uses_dead_wall() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {players:[{hand:{tiles:[], melds:[]}, river:[]}], wall:{tiles:[{suit:'pin', value:1}], dead_wall:[{suit:'sou', value:9}]}, dead_wall:[{suit:'sou', value:9}]};\n"
        "const meldEvt = {name:'meld', payload:{player_index:0, meld:{tiles:[{suit:'pin',value:1},{suit:'pin',value:1},{suit:'pin',value:1},{suit:'pin',value:1}], type:'kan'}}};\n"
        "const afterMeld = applyEvent(state, meldEvt);\n"
        "const drawEvt = {name:'draw_tile', payload:{player_index:0, tile:{suit:'sou', value:9}}};\n"
        "const next = applyEvent(afterMeld, drawEvt);\n"
        "console.log(next.wall.tiles.length + ':' + next.dead_wall.length + ':' + next.wall.dead_wall.length);"
    )
    output = run_node(code)
    assert output == '1:0:0'


def test_skip_updates_current_player() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {current_player: 0, players: [{}, {}], waiting_for_claims:[0]};\n"
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


def test_meld_removes_discard_from_river() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {last_discard:{suit:'man',value:1}, last_discard_player:0, \n"
        "players:[\n"
        "  {hand:{tiles:[], melds:[]}, river:[{suit:'man',value:1}]},\n"
        "  {hand:{tiles:[{suit:'man',value:2},{suit:'man',value:3}], melds:[]}, river:[]}\n"
        "]};\n"
        "const evt = {name:'meld', payload:{player_index:1, meld:{tiles:[{suit:'man',value:1},{suit:'man',value:2},{suit:'man',value:3}], type:'chi', called_index:0}}};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.players[0].river.length + ':' + newState.players[1].hand.melds.length + ':' + newState.last_discard);"
    )
    output = run_node(code)
    assert output == '0:1:null'

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


def test_tsumo_sets_result_and_scores() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {players:[{score:25000},{score:25000},{score:25000},{score:25000}]};\n"
        "const evt = {name:'tsumo', payload:{player_index:0, scores:[26000,24000,24000,24000], result:{han:1,fu:30,cost:{total:1000}}, win_tile:{suit:'man',value:1}, hand:{tiles:[],melds:[]}}};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.result.type + ':' + newState.players[0].score);"
    )
    output = run_node(code)
    assert output == 'tsumo:26000'


def test_ron_sets_result_and_scores() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {players:[{score:25000},{score:25000},{score:25000},{score:25000}]};\n"
        "const evt = {name:'ron', payload:{player_index:0, scores:[33000,17000,25000,25000], result:{han:2,fu:40,cost:{total:8000}}, win_tile:{suit:'pin',value:5}, hand:{tiles:[],melds:[]}}};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.result.type + ':' + newState.players[0].score);"
    )
    output = run_node(code)
    assert output == 'ron:33000'


def test_claims_closed_clears_waiting_for_claims() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {waiting_for_claims:[0,1]};\n"
        "const evt = {name:'claims_closed'};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.waiting_for_claims.length);"
    )
    output = run_node(code)
    assert output == '0'


def test_skip_ignored_when_not_waiting() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {current_player:0, players:[{}, {}], waiting_for_claims:[]};\n"
        "const evt = {name:'skip', payload:{player_index:0}};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.current_player + ':' + newState.waiting_for_claims.length);"
    )
    output = run_node(code)
    assert output == '0:0'


def test_round_end_keeps_result() -> None:
    code = (
        "import { applyEvent } from './web_gui/applyEvent.js';\n"
        "const state = {result:{type:'tsumo'}};\n"
        "const evt = {name:'round_end'};\n"
        "const newState = applyEvent(state, evt);\n"
        "console.log(newState.result.type);"
    )
    output = run_node(code)
    assert output == 'tsumo'
