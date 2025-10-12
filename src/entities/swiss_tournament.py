from src.entities.tournament import Tournament
from src.entities.time_control import TimeControl

from src.utils.decorators import type_check

class SwissTournament(Tournament):
    """Class representing a Swiss-system chess tournament."""
    @type_check
    def __init__(self, name: str, location: str, start_date: str, end_date: str, time_control: TimeControl, rounds: int):
        """
        Initialize a SwissTournament instance.

        Args:
            name (str): The name of the tournament.
            location (str): The location of the tournament.
            start_date (str): The start date of the tournament in 'YYYY-MM-DD' format.
            end_date (str): The end date of the tournament in 'YYYY-MM-DD' format.
            time_control (TimeControl): The time control of the tournament.
            rounds (int): The number of rounds in the Swiss tournament.
        """
        super().__init__(name, location, start_date, end_date, time_control)
        self.__rounds = rounds  # Number of rounds in the Swiss tournament

    @property
    def rounds(self) -> int:
        """Get the number of rounds in the Swiss tournament."""
        return self.__rounds
    
    @rounds.setter
    def rounds(self, value: int):
        """Set the number of rounds in the Swiss tournament."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Number of rounds must be a positive integer.")
        self.__rounds = value