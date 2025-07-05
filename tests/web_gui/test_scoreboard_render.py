import subprocess


def run_node(code: str) -> str:
    result = subprocess.run(
        ["node", "-e", code], capture_output=True, text=True, cwd="web_gui"
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_scoreboard_renders() -> None:
    output = run_node(
        "import React from 'react';\n"
        "import { renderToStaticMarkup } from 'react-dom/server';\n"
        "import ScoreBoard from './ScoreBoard.js';\n"
        "const players = [\n"
        "  { name: 'Alice', seat_wind: 'east', score: 25000 },\n"
        "  { name: 'Bob', seat_wind: 'south', score: 24000 },\n"
        "];\n"
        "const html = renderToStaticMarkup(\n"
        "  React.createElement(ScoreBoard, { players })\n"
        ");\n"
        "console.log(html);"
    )
    assert 'Alice' in output
    assert 'east' in output
    assert '25000' in output
