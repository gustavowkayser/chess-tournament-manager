from src.entities.player import Player

from src.utils.decorators import type_check

class Game:
    """Class representing a chess game between two players."""
    @type_check
    def __init__(self, white: Player, black: Player):
        """
        Initialize a Game instance.

        Args:
            white (Player): The player with the white pieces.
            black (Player): The player with the black pieces.
        """
        self.__white = white
        self.__black = black
        self.__result: str | None = None  # Possible values: "1-0", "0-1", "0.5-0.5"

    @property
    def white(self) -> Player:
        """Get the player with the white pieces."""
        return self.__white
    
    @white.setter
    def white(self, value: Player):
        """Set the player with the white pieces."""
        if not isinstance(value, Player):
            raise ValueError("White player must be an instance of Player.")
        self.__white = value

    @property
    def black(self) -> Player:
        """Get the player with the black pieces."""
        return self.__black
    
    @black.setter
    def black(self, value: Player):
        """Set the player with the black pieces."""
        if not isinstance(value, Player):
            raise ValueError("Black player must be an instance of Player.")
        self.__black = value

    @property
    def result(self) -> str | None:
        """Get the result of the game."""
        return self.__result
    
    @result.setter
    def result(self, value: str | None):
        """Set the result of the game."""
        if value not in ["1-0", "0-1", "0.5-0.5", None]:
            raise ValueError("Result must be '1-0', '0-1', '0.5-0.5', or None.")
        self.__result = value