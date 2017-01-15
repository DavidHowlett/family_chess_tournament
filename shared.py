"""This file contains the exceptions shared by the AI and the runner.
They could live in the runner but avoiding
circular dependencies is desirable."""


class Draw(Exception):
    """Please throw one of the specific exceptions to call a draw."""
    pass


class StalemateException(Draw):
    """To be thrown by the AIs when a stalemate is encountered."""
    pass


class ThreeFoldRepetition(Draw):
    """Throw this when you want to declare a draw due to the three fold repetition rule."""
    pass


class FiftyMoveException(Draw):
    """Throw this when you want to call a draw using the 50 move rule."""
    pass
