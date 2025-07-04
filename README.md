# MyMahjong

MyMahjong is a simple TypeScript monorepo for experimenting with a Mahjong game engine and related tooling.  The repository is intentionally small so the entire system can be understood at a glance.  It contains three packages:

- **core** – the game logic such as tiles, players and wall implementation
- **cli** – a command line interface for playing the game in the terminal
- **web** – a minimal web layer that demonstrates using the core package

## Implementation status

The repository currently includes initial engine modules in the **core**
package. Future work will expand these components. Other packages remain stubbed.

### Packages

 - [x] core
 - [ ] cli
 - [x] web
 - [x] web_gui

### Features

- [ ] Mortal AI integration
- [x] Mortal backend integration design
- [ ] MJAI protocol support
- [ ] Local single-player play via CLI
- [ ] REST + WebSocket API
- [x] Basic REST endpoints (create game, fetch game, health)
- [x] Web GUI served through GitHub Pages
- [x] Basic GUI status display
- [x] Continuous integration workflow
- [x] Core <-> interface API documented
- [x] GUI design documented

### Core engine capabilities

- [x] start_game
- [x] draw_tile
- [x] discard_tile
- [x] get_state
- [x] scoring
- [x] call_chi
- [x] call_pon
- [x] call_kan
- [x] declare_tsumo
- [x] declare_ron
- [x] skip
- [x] end_game

## Implementation plan

1. **Create the game engine** – wrap the Python `mahjong` library and expose
   methods for drawing, discarding and scoring.
2. **Integrate Mortal AI** – add a module that uses the
   [MJAI high level API](https://mjai.app/docs/highlevel-api) to communicate with
   the AI process and execute its moves.
3. **Build CLI** – provide commands for starting a local game against the AI and
   for connecting to remote games.
4. **Implement FastAPI server** – expose REST and WebSocket endpoints for game
   management and real-time play.
5. **Develop React front-end** – consume the API and present a board based on the
   `docs/board-layout.md` design.
6. **Implement MJAI adapter** – translate game state to and from
   `docs/mjai-ai-integration.md` so AI engines can connect via the protocol.
7. **Set up GitHub Actions** – lint, type check, run tests and deploy the built
   web front-end to GitHub Pages.

See `docs/detailed-design.md` for an overview of the planned architecture.
`docs/web-gui-architecture.md` provides more details about the planned React GUI.

## Deployed to

The static web GUI in the `web_gui` directory is built and deployed via GitHub Pages:

https://kotarotanabe.github.io/MyMahjong/

## Continuous Integration

GitHub Actions run linting, type checking, build and tests for every pull request.
Once these checks succeed, the workflow automatically approves and merges the PR.
