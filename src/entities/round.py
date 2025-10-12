from src.utils.decorators import type_check

class Round:
    """Class representing a round in a tournament."""
    @type_check
    def __init__(self, round_: int, subround: int = 0):
        """
        Initialize a Round instance.

        Args:
            round_ (int): The round number.
            subround (int): The subround number (default is 0).
        """
        self.__round = round_
        self.__subround = subround
        self.__matches = []  # List to hold matches (games) in the round

    @property
    def round_(self) -> int:
        """Get the round number."""
        return self.__round

    @round_.setter
    def round_(self, value: int):
        """Set the round number."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Round number must be a positive integer.")
        self.__round = value

    @property
    def subround(self) -> int:
        """Get the subround number."""
        return self.__subround
    
    @subround.setter
    def subround(self, value: int):
        """Set the subround number."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("Subround number must be a non-negative integer.")
        self.__subround = value

    @property
    def matches(self) -> list:
        """Get the list of matches (games) in the round."""
        return self.__matches

    @matches.setter
    def matches(self, value: list):
        """Set the list of matches (games) in the round."""
        if not isinstance(value, list):
            raise ValueError("Matches must be a list.")
        self.__matches = value

    def add_match(self, game):
        """
        Add a match (game) to the round.

        Args:
            game: The Game object to add.
        """
        from src.entities.game import Game
        if not isinstance(game, Game):
            raise ValueError("Only Game objects can be added as matches.")
        self.__matches.append(game)

    def get_match_count(self) -> int:
        """
        Get the number of matches in this round.

        Returns:
            int: Number of matches.
        """
        return len(self.__matches)
