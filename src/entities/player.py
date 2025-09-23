from src.entities.rating import Rating

from src.utils.decorators import type_check

class Player:
    """Class representing a player in the chess tournament."""
    @type_check
    def __init__(self, name: str, birthdate: str, gender: str, rating: Rating):
        """
        Initialize a Player instance.

        Args:
            name (str): The name of the player.
            birthdate (str): The birthdate of the player in 'YYYY-MM-DD' format.
            gender (str): The gender of the player.
            rating (Rating): The rating of the player.
        """
        self.__name = name
        self.__birthdate = birthdate
        self.__gender = gender
        self.__rating = rating

    @property
    def name(self) -> str:
        """Get the player's name."""
        return self.__name
    
    @name.setter
    def name(self, value: str):
        """Set the player's name."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string.")
        self.__name = value.strip()

    @property
    def birthdate(self) -> str:
        """Get the player's birthdate."""
        return self.__birthdate
    
    @birthdate.setter
    def birthdate(self, value: str):
        """Set the player's birthdate."""
        # Basic validation for 'YYYY-MM-DD' format
        if not isinstance(value, str) or len(value) != 10 or value[4] != '-' or value[7] != '-':
            raise ValueError("Birthdate must be a string in 'YYYY-MM-DD' format.")
        self.__birthdate = value

    @property
    def gender(self) -> str:
        """Get the player's gender."""
        return self.__gender
    
    @gender.setter
    def gender(self, value: str):
        """Set the player's gender."""
        if not isinstance(value, str) or value.strip() not in ["male", "female", "other"]:
            raise ValueError("Gender must be 'male', 'female', or 'other'.")
        self.__gender = value.strip()

    @property
    def rating(self) -> Rating:
        """Get the player's rating."""
        return self.__rating
    
    @rating.setter
    def rating(self, value: Rating):
        """Set the player's rating."""
        if not isinstance(value, Rating):
            raise ValueError("Rating must be an instance of the Rating class.")
        self.__rating = value