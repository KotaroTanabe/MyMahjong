import subprocess


def run_node(code: str) -> str:
    result = subprocess.run(
        ["node", "-e", code], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_start_kyoku_resets_state() -> None:
    code = (
        "import { applyEvent } from './web_gui/eventHandlers.js';\n"
        "const prev = {wall:{tiles:[1,2,3]}, players:[{hand:{tiles:[{suit:'man',value:1}]}, river:[]} ]};\n"
        "const newState = {wall:{tiles:[0,0]}, players:[{hand:{tiles:[]}, river:[]} ]};\n"
        "const evt = {name:'start_kyoku', payload:{state:newState}};\n"
        "const result = applyEvent(prev, evt);\n"
        "console.log(result.wall.tiles.length + ':' + result.players[0].hand.tiles.length);"
    )
    output = run_node(code)
    assert output == '2:0'

