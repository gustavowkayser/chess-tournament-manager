from src.utils.decorators import type_check

class Rating:
    """Class representing a player's rating in different time controls."""
    @type_check
    def __init__(self, classic: int, rapid: int, blitz: int):
        """
        Initialize a Rating instance.

        Args:
            classic (int): The player's classical rating.
            rapid (int): The player's rapid rating.
            blitz (int): The player's blitz rating.
        """
        self.__classic = classic
        self.__rapid = rapid
        self.__blitz = blitz

    @property
    def classic(self) -> int:
        """Get the classical rating."""
        return self.__classic
    
    @classic.setter
    def classic(self, value: int):
        """Set the classical rating."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("Classical rating must be a non-negative integer.")
        self.__classic = value

    @property
    def rapid(self) -> int:
        """Get the rapid rating."""
        return self.__rapid
    
    @rapid.setter
    def rapid(self, value: int):
        """Set the rapid rating."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("Rapid rating must be a non-negative integer.")
        self.__rapid = value

    @property
    def blitz(self) -> int:
        """Get the blitz rating."""
        return self.__blitz
    
    @blitz.setter
    def blitz(self, value: int):
        """Set the blitz rating."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("Blitz rating must be a non-negative integer.")
        self.__blitz = value