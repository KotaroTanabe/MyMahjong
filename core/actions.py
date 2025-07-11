"""Definitions for core action strings."""

__all__ = [
    "DRAW",
    "DISCARD",
    "CHI",
    "PON",
    "KAN",
    "RIICHI",
    "TSUMO",
    "RON",
    "SKIP",
    "START_KYOKU",
    "ADVANCE_HAND",
    "END_GAME",
    "VALID_ACTIONS",
]

DRAW = "draw"
"""Draw a tile from the wall."""

DISCARD = "discard"
"""Discard a tile from the hand."""

CHI = "chi"
"""Call chi on the last discard."""

PON = "pon"
"""Call pon on the last discard."""

KAN = "kan"
"""Declare an open or closed kan."""

RIICHI = "riichi"
"""Declare riichi after discarding a tile."""

TSUMO = "tsumo"
"""Declare a self-drawn win."""

RON = "ron"
"""Declare a win on another player's discard."""

SKIP = "skip"
"""Pass on claiming the last discard."""

START_KYOKU = "start_kyoku"
"""Start a new hand at the given dealer and round number."""

ADVANCE_HAND = "advance_hand"
"""Advance the dealer marker without playing a hand."""

END_GAME = "end_game"
"""End the current game."""

# All valid action strings understood by :mod:`core.api.apply_action`.
VALID_ACTIONS = [
    DRAW,
    DISCARD,
    CHI,
    PON,
    KAN,
    RIICHI,
    TSUMO,
    RON,
    SKIP,
    START_KYOKU,
    ADVANCE_HAND,
    END_GAME,
]
