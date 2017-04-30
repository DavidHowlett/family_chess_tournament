"""This file contains the exceptions shared by the AI and the runner.
They could live in the runner but avoiding
circular dependencies is desirable."""


class ThreeFoldRepetition(Exception):
    """Throw this when you want to declare a draw due to the three fold repetition rule."""
    pass


class FiftyMoveException(Exception):
    """Throw this when you want to call a draw using the 50 move rule."""
    pass
