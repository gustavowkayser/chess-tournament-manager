from src.utils.decorators import type_check

class Tournament:
    """Class representing a chess tournament."""
    @type_check
    def __init__(self, name: str, location: str, start_date: str, end_date: str):
        """
        Initialize a Tournament instance.

        Args:
            name (str): The name of the tournament.
            location (str): The location of the tournament.
            start_date (str): The start date of the tournament in 'YYYY-MM-DD' format.
            end_date (str): The end date of the tournament in 'YYYY-MM-DD' format.
        """
        self.__name = name
        self.__location = location
        self.__start_date = start_date
        self.__end_date = end_date

        self.__players = []  # List to hold players participating in the tournament
        self.__rounds = []   # List to hold rounds in the tournament

    @property
    def name(self) -> str:
        """Get the tournament's name."""
        return self.__name
    
    @name.setter
    def name(self, value: str):
        """Set the tournament's name."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Tournament name must be a non-empty string.")
        self.__name = value.strip()

    @property
    def location(self) -> str:
        """Get the tournament's location."""
        return self.__location
    
    @location.setter
    def location(self, value: str):
        """Set the tournament's location."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Location must be a non-empty string.")
        self.__location = value.strip()

    @property
    def start_date(self) -> str:
        """Get the tournament's start date."""
        return self.__start_date
    
    @start_date.setter
    def start_date(self, value: str):
        """Set the tournament's start date."""
        # Basic validation for 'YYYY-MM-DD' format
        if not isinstance(value, str) or len(value) != 10 or value[4] != '-' or value[7] != '-':
            raise ValueError("Start date must be a string in 'YYYY-MM-DD' format.")
        self.__start_date = value

    @property
    def end_date(self) -> str:
        """Get the tournament's end date."""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: str):
        """Set the tournament's end date."""
        # Basic validation for 'YYYY-MM-DD' format
        if not isinstance(value, str) or len(value) != 10 or value[4] != '-' or value[7] != '-':
            raise ValueError("End date must be a string in 'YYYY-MM-DD' format.")
        self.__end_date = value