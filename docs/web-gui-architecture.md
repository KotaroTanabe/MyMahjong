# Web GUI Architecture

This document outlines the planned front-end architecture for the MyMahjong web interface. It expands on the layout guidelines in [board-layout.md](./board-layout.md) and the principles in [gui-design.md](./gui-design.md).

## Overview

The web client will be implemented as a small React application bundled with Vite. The application connects to the FastAPI backend via REST calls for basic actions and a WebSocket for real-time updates. Game data mirrors the `GameState` model from the `core` package.

## Component Hierarchy

- **App** – top-level component that sets up routing and the WebSocket connection.
- **GameBoard** – renders the table layout, player areas and central indicators.
- **Hand** – displays the tiles in a player's hand and action buttons.
- **River** – shows each player's discard pile with orientation classes.
- **MeldArea** – lists called sets (chi/pon/kan) for a seat.
- **Controls** – buttons for calling melds, declaring wins and skipping turns.

Each component receives only the data it needs so the interface remains simple and testable. Styling is handled by a single `style.css` file using CSS grid and flexbox.

## Data Flow

1. After the page loads, `App` fetches the current game state via `GET /games/{id}`.
2. `App` opens a WebSocket to `/ws/{id}` and listens for events.
3. Incoming events update the React state, which re-renders the `GameBoard`.
   When the engine sends a `draw_tile` event with `source: "dead_wall"` (after a
   kan), the tile is inserted into the acting player's hand before further
   actions are offered.
4. The GUI queries `/games/{id}/next-actions` to determine which player acts next
   and what actions are possible. The set of allowed actions for each player is
   pushed to the client via an `allowed_actions` WebSocket event, so no extra
   requests are needed when claims are possible.
   Helper functions like `getAllowedActions` and `getNextActions` require a
   unique `requestId` so in-flight calls can be cancelled. Components should pass
   a stable id and clean up controllers when unmounting.
5. If the only action is `draw`, the server performs it automatically and returns
   the subsequent player instead.
6. Otherwise the GUI checks if that player is AI-controlled and either requests
   an AI move or enables the relevant buttons for a human.
7. User or AI actions are sent back via `POST /games/{id}/action`.

## Future Enhancements

- Persist player sessions so reconnects restore the current hand.
- Animate tile movements with CSS transitions.
- Provide accessibility labels for screen readers.

This architecture keeps the front-end lightweight while leaving room for more advanced features as the project evolves.
