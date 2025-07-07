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


def test_format_next_actions_event() -> None:
    code = (
        "import { formatEvent } from './web_gui/eventLog.js';\n"
        "const evt = {name:'next_actions', payload:{player_index:2, actions:['draw','discard']}};\n"
        "console.log(formatEvent(evt));"
    )
    output = run_node(code)
    assert output.startswith('Next actions for player 2')


def test_event_to_mjai_json() -> None:
    code = (
        "import { eventToMjaiJson } from './web_gui/eventLog.js';\n"
        "const evt = {name:'discard', payload:{player_index:1, tile:{suit:'pin', value:3}}};\n"
        "console.log(eventToMjaiJson(evt));"
    )
    output = run_node(code)
    assert '"type":"discard"' in output
    assert '"player_index":1' in output


def test_format_claims_closed() -> None:
    code = (
        "import { formatEvent } from './web_gui/eventLog.js';\n"
        "console.log(formatEvent({name:'claims_closed'}));"
    )
    output = run_node(code)
    assert output.startswith('捨て牌に対するアクションはありませんでした')
