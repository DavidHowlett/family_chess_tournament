"""This file contains the exceptions shared by the AI and the runner.
They could live in the runner but avoiding
circular dependencies is desirable."""


class StalemateException(Exception):
    """To be thrown by the AIs when a stalemate is encountered."""
    pass


class ThreeFoldRepetition(Exception):
    """Throw this when you want to declare a draw due to the three fold repetition rule"""
    pass