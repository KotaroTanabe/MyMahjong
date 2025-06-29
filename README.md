# MyMahjong

MyMahjong is a simple TypeScript monorepo for experimenting with a Mahjong game engine and related tooling.  The repository is intentionally small so the entire system can be understood at a glance.  It contains three packages:

- **core** – the game logic such as tiles, players and wall implementation
- **cli** – a command line interface for playing the game in the terminal
- **web** – a minimal web layer that demonstrates using the core package

## Deployed to

https://kotarotanabe.github.io/MyMahjong/

### GitHub Pages

Running `npm run build` from the repository root compiles every package and
produces static files for the web demo under `web/dist`. The CI workflow deploys
those files to GitHub Pages using
[peaceiris/actions-gh-pages](https://github.com/peaceiris/actions-gh-pages).
You can preview the built site locally with:

```bash
npm run build
npm run preview -w web
```

The web build uses the repository name as its base path so assets resolve
correctly on GitHub Pages. If you fork this project, update `web/vite.config.ts`
to use your repository name.


## Overview

The **core** package models tiles, player hands and the wall.  The **cli**
package provides a simple terminal interface for a few demonstration turns, and
the **web** package shows how the same logic can drive a React app.  Feel free
to expand the rules or presentation layer to suit your needs.

## Implementation Status

### core

- [x] Tile generation, drawing, discarding and win detection
- [x] Scoring for yaku: `tanyao`, `chiitoitsu`, `yakuhai`, `toitoi`, `iipeikou`, `ittsu`, `pinfu`, `dora`, `riichi`
- [x] Dealer rotation and round wind progression
- [ ] Additional yaku and detailed fu/han calculations
- [ ] Other advanced rules

### cli

- [x] Single-player demo showing possible yaku
- [ ] Colored output
- [ ] Unicode tile graphics
- [ ] Full game flow

### web (gui)

- [x] Board layout with dora indicators and wall display
- [x] Interactive hand for the bottom player with responsive layout
- [ ] Richer graphics
- [ ] Full interaction for all players
- [ ] Features described in `docs/gui-design.md`

## Getting Started

### Install Dependencies

Use [Node.js](https://nodejs.org/) and install dependencies for all workspaces from the repository root:

```bash
npm install
```

### Build

Compile all TypeScript packages using:

```bash
npm run build
```

You can also build a specific workspace by passing the `-w` option. For example
the following will compile only the core package:

```bash
npm run build -w core
```
### Running the CLI

Build and launch the command line interface:

```bash
npm run build -w cli
npm start -w cli
```

### Running the Web Demo

Start the Vite development server:

```bash
npm run dev -w web
```

Then open `http://localhost:5173` in your browser.

The board layout places each player's area around the center. Discards are displayed as a traditional 河 with tiles aligned per seat. At this stage only
the bottom player shows the actual hand and discard pile. Further layout details
are described in [docs/board-layout.md](docs/board-layout.md).

### Custom Game Setup

The `useGame` hook accepts an optional `Game` instance. This is handy for tests
or when you want to provide a pre-configured wall of tiles. If no game is
provided, `useGame` creates a new one and deals the first player.

### Scoring

After each discard the game now evaluates your hand for the simple `tanyao` yaku
and checks for `chiitoitsu` (seven pairs). The scorer also detects `yakuhai`
triplets of winds or dragons.
When applicable, the CLI and web UI display the possible yaku, the number of han
and total points.

### Rule Coverage

The core engine implements only a small slice of Mahjong. Below is the current
status and a suggested roadmap for extending the rules.

**Implemented**

- [x] Generation of all 136 tiles and shuffled wall
- [x] Dealing, drawing and discarding tiles
- [x] Basic win detection for standard hands
- [x] Win by ron (claiming another player's discard)
- [x] Ability to call pon, chi and kan (melds)
- [x] Replacement tile draw and extra dora indicator after kan
- [x] Scoring for:
  - [x] `tanyao` (all simples)
  - [x] `chiitoitsu` (seven pairs)
  - [x] `yakuhai` triplets of winds or dragons
  - [x] `toitoi` (all triplets)
  - [x] `iipeikou` (two identical sequences)
  - [x] `ittsu` (straight 1-9 in one suit)
  - [x] `pinfu` (all sequences with no extra fu)
  - [x] `dora` bonus tiles from indicators
  - [x] `riichi` declaration
  - [x] Seat wind assignment and dealer rotation
- [x] Round progression with changing round winds

**Not Yet Implemented**

- [ ] Additional yaku and detailed fu/han scoring
- [ ] Other advanced rules (kan-based yaku, etc.)

**Recommended Next Steps**

1. Expand the scoring system with more yaku and fu calculations
2. Add support for advanced rules beyond riichi

## Implementation Plan: Full Game Loop

Below is a high-level roadmap for integrating the **core** package with the
web GUI so that one complete game can be played:

1. **Expand the Game Loop** – create a round/hand sequence using
   `Game.nextHand()` and `Game.rotateDealer()`.
   Update the `useGame` hook to start new hands and advance the round.
2. **Handle Multiple Players** – implement lightweight AI logic for the other
   seats. Expose each hand and meld area in `GameBoard`, keeping opponents'
   tiles hidden.
3. **Win Conditions and Scoring** – after every action check
   `Game.isWinningHand()` or `Game.declareRon()` and display results in
   `ScoreBoard` before rotating to the next dealer or round.
4. **UI Enhancements** – follow `docs/board-layout.md` for a stable table and
   tackle the items in `docs/gui-design.md` such as icon controls and responsive
   units.
5. **State Synchronization** – ensure `useGame` refreshes state after each draw,
   discard or call so React consistently re-renders, and keep the scoreboard in
   sync.
6. **Testing** – extend the existing `useGame` tests to cover the new game loop
   and AI decisions.


### Run Tests

Tests are written with Node's built‑in `node:test` runner. Build and run tests for every package with:

```bash
npm test
```

Individual workspaces can be tested using `-w` as well. The command below runs only the CLI tests:

```bash
npm test -w cli
```

### Package Layout

```
core/  – reusable game engine
cli/   – terminal interface using the core package
web/   – example web package also using the core package
```

Each package has its own `package.json` and `tsconfig.json`. The root
`package.json` defines npm workspaces so the packages can reference each other
without publishing to a registry. Source lives in the `src` folders and compiled
JavaScript is emitted to `dist` when you run the build script.

## Continuous Integration

GitHub Actions run linting, type checking, build and tests for every pull request.
Once these checks succeed, the workflow automatically approves and merges the PR.

## Contributing

This repository is provided as a demonstration of Codex. We are not accepting
external pull requests or commits. If you have questions or suggestions, feel
free to open an issue.

