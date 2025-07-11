"""Action name constants used across packages."""
CHI = "chi"
PON = "pon"
KAN = "kan"
RIICHI = "riichi"
TSUMO = "tsumo"
RON = "ron"
SKIP = "skip"
DRAW = "draw"
DISCARD = "discard"
START_KYOKU = "start_kyoku"
ADVANCE_HAND = "advance_hand"
END_GAME = "end_game"
AUTO = "auto"

# List of valid actions recognized by the API and web server
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
    AUTO,
]
