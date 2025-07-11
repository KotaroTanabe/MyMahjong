"""Custom exceptions for the core package."""

class InvalidActionError(Exception):
    """Raised when a player attempts an invalid action."""


class NotYourTurnError(InvalidActionError):
    """Raised when a player acts out of turn."""

