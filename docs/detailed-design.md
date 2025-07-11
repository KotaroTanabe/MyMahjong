# Detailed Design

This document outlines the planned architecture and major components of the MyMahjong project. The goal is to provide enough structure for implementation while keeping the design flexible for future enhancements.

## Overview

MyMahjong is organized as a monorepo containing three top-level packages:

- **core** – Python engine that wraps the `mahjong` library
- **cli** – simple terminal interface built with Click
- **web** – FastAPI server with a React front-end

Each package will remain independent so they can be developed and published separately. Shared data models will live in the `core` package.

## Core Package

The core engine exposes the game state and fundamental operations. It is designed for reuse by both the CLI and the web server. Key modules are:

| Module | Responsibility |
| --- | --- |
| `mahjong_engine.py` | Wraps the `mahjong` library and tracks the overall game state. Provides methods such as `draw_tile`, `discard_tile`, `call_pon`, and `calculate_score`. |
| `player.py` | Represents a player seat. Handles hand tiles, melds, score, and seat wind. |
| `wall.py` | Manages the tile wall, dead wall, and dora indicators. |
| `ai_adapter.py` | Optional module that converts game state to and from the MJAI protocol. |

### Data Model

The engine defines classes for `Tile`, `Hand`, `Meld`, and `GameState`. All messages exchanged with external AIs or the web client will serialize these classes to JSON.

### Extensibility

To simplify future rule variations or scoring tweaks, the engine will encapsulate all rule logic in dedicated classes. A `RuleSet` interface provides methods for determining valid moves and scoring patterns. Implementations can extend this to support different variants of Mahjong.

## CLI Package

The CLI package provides a basic local interface so developers can play against an AI or another human. Major files include:

| File | Description |
| --- | --- |
| `main.py` | Entrypoint with Click commands such as `start` and `join`. |
| `local_game.py` | Runs a single-player game loop using the core engine and AI adapter. |

Gameplay occurs entirely in the terminal. The CLI will eventually expose commands to connect to remote servers or spectate ongoing games.

## Web Package

The web package combines a FastAPI backend with a React front-end. They are bundled together so the same repository hosts both the API and the static site.

### Backend

The backend exposes REST endpoints for managing games and a WebSocket for real-time updates. Primary routes include:

- `POST /games` – create a new game
- `GET /games/{id}` – fetch current state
- `POST /games/{id}/action` – submit a player action (draw, discard, etc.)
- `GET /ws/{id}` – connect to the game's WebSocket stream

The backend imports the core engine to enforce all game rules and transitions. It also provides an MJAI adapter endpoint so external AIs can participate.

### Front-end

The front-end is a simple React application. It communicates with the FastAPI server using the REST and WebSocket APIs. Components correspond to sections in `board-layout.md` and adhere to the responsive guidelines in `gui-design.md`.

The interface renders tiles using SVG images and displays player hands, discard piles, and melds. Controls allow a local player to draw, discard, or call melds. The React state mirrors the `GameState` object provided by the backend.

## MJAI Adapter

The adapter converts engine events into the [MJAI protocol](https://mjai.app/docs/highlevel-api) so external Mahjong AIs can make decisions. This module is optional and can be enabled when running against an external AI engine.

Key responsibilities:

1. Translate internal game events into MJAI JSON messages.
2. Send those messages to the AI over STDIN/STDOUT or WebSocket.
3. Validate and apply the AI's responses within the engine.

This layer allows the CLI and web server to run AI opponents without embedding AI logic directly in the project.

## Build and Test Strategy

The repository now contains several Python packages along with a React front-end. Continuous integration runs flake8 and mypy, builds the packages, and executes unit tests including the GUI's Vitest suite. A single GitHub Actions workflow installs all dependencies with `uv` and verifies every package before merging changes.

---

This design provides a foundation for implementing a full-featured Mahjong platform while remaining modular and easy to extend.
