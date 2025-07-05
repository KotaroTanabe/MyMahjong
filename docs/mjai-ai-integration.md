# MJAI AI Integration

This project aims to run external Mahjong AIs that communicate via the [MJAI high level API](https://mjai.app/docs/highlevel-api). Our engine will expose an adapter that converts game state into the JSON messages defined by the specification and consumes the responses produced by the AI process. The goal is to support any AI that follows this protocol.

Key points:

- The engine starts the AI as a separate process and exchanges messages over STDIN/STDOUT or a WebSocket.
- Messages include actions such as `start_game`, `end_game`, `draw_tile`, and decisions like `discard_tile`.
- The adapter will validate incoming messages and translate them into engine calls.

This integration makes it possible to plug different AI engines into both the CLI and web server.
