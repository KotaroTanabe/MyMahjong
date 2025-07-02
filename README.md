# MyMahjong

MyMahjong is a simple TypeScript monorepo for experimenting with a Mahjong game engine and related tooling.  The repository is intentionally small so the entire system can be understood at a glance.  It contains three packages:

- **core** – the game logic such as tiles, players and wall implementation
- **cli** – a command line interface for playing the game in the terminal
- **web** – a minimal web layer that demonstrates using the core package

## Deployed to

https://kotarotanabe.github.io/MyMahjong/

## Continuous Integration

GitHub Actions run linting, type checking, build and tests for every pull request.
Once these checks succeed, the workflow automatically approves and merges the PR.

## Contributing

This repository is provided as a demonstration of Codex. We are not accepting
external pull requests or commits.
