# Remaining Core Tasks

The following features are still missing from the `core` package to allow a full Mahjong game. Each item should be implemented incrementally.

## Closed and added kans
- Allow players to declare a closed kan using four tiles from their hand.
- Support added kan (shouminkan) when a player upgrades a pon meld.
- Draw a replacement tile from the dead wall and reveal a new dora indicator.
- Emit chankan opportunities for other players.

## Honba and riichi stick tracking
- Track the number of bonus points on the table for consecutive draws/wins.
- Deduct and pay out riichi sticks when wins are resolved.

## Round progression and renchan
- Advance the round and dealer position automatically after each hand.
- Handle dealer repeats when the dealer wins or the hand ends in draw.
- Detect the end of a hanchan.

## Exhaustive draw conditions
- Detect rare draw scenarios such as four kans, four riichi, and nine terminals.
- Emit a `ryukyoku` event with the specific reason.

## MJAI protocol adapter
- Expand `ai_adapter.py` to handle all MJAI messages.
- Validate actions received from external AIs before applying them.

## Mortal AI integration
- Use `mortal_runner.py` to launch the AI and connect through the adapter.
- Provide helpers so the CLI and web server can run Mortal as an opponent.

