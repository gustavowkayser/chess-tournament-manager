from src.utils.decorators import type_check
from src.entities.time_control import TimeControl

class Tournament:
    """Class representing a chess tournament."""
    @type_check
    def __init__(self, name: str, location: str, start_date: str, end_date: str, time_control: TimeControl):
        """
        Initialize a Tournament instance.

        Args:
            name (str): The name of the tournament.
            location (str): The location of the tournament.
            start_date (str): The start date of the tournament in 'YYYY-MM-DD' format.
            end_date (str): The end date of the tournament in 'YYYY-MM-DD' format.
            time_control (TimeControl): The time control of the tournament.
        """
        self.__name = name
        self.__location = location
        self.__start_date = start_date
        self.__end_date = end_date
        self.__time_control = time_control

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

    @property
    def time_control(self) -> TimeControl:
        """Get the tournament's time control."""
        return self.__time_control
    
    @time_control.setter
    def time_control(self, value: TimeControl):
        """Set the tournament's time control."""
        if not isinstance(value, TimeControl):
            raise ValueError("Time control must be a TimeControl enum.")
        self.__time_control = value

    @property
    def players(self) -> list:
        """Get the list of players in the tournament."""
        return self.__players.copy()

    def add_player(self, player):
        """
        Add a player to the tournament.

        Args:
            player: The player to add to the tournament.

        Raises:
            ValueError: If player is already registered in the tournament.
        """
        from src.entities.player import Player
        if not isinstance(player, Player):
            raise ValueError("Only Player objects can be added to the tournament.")
        
        # Check if player is already registered
        if any(p.name == player.name for p in self.__players):
            raise ValueError(f"Player '{player.name}' is already registered in this tournament.")
        
        self.__players.append(player)

    def remove_player(self, player_name: str):
        """
        Remove a player from the tournament by name.

        Args:
            player_name (str): The name of the player to remove.

        Raises:
            ValueError: If player is not found in the tournament.
        """
        initial_length = len(self.__players)
        self.__players = [p for p in self.__players if p.name != player_name]
        
        if len(self.__players) == initial_length:
            raise ValueError(f"Player '{player_name}' not found in this tournament.")

    def get_players_by_rating(self, rating_type: str = 'classic') -> list:
        """
        Get players sorted by rating in descending order.

        Args:
            rating_type (str): The type of rating to sort by ('classic', 'rapid', or 'blitz').

        Returns:
            list: List of players sorted by rating (highest to lowest).
        """
        if rating_type not in ['classic', 'rapid', 'blitz']:
            raise ValueError("Rating type must be 'classic', 'rapid', or 'blitz'.")
        
        return sorted(
            self.__players,
            key=lambda p: getattr(p.rating, rating_type),
            reverse=True
        )
