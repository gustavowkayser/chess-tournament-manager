from src.entities.tournament import Tournament
from src.entities.time_control import TimeControl

from src.utils.decorators import type_check

class EliminatoryTournament(Tournament):
    """Class representing an eliminatory chess tournament."""
    @type_check
    def __init__(self, name: str, location: str, start_date: str, end_date: str, time_control: TimeControl):
        """
        Initialize an EliminatoryTournament instance.

        Args:
            name (str): The name of the tournament.
            location (str): The location of the tournament.
            start_date (str): The start date of the tournament in 'YYYY-MM-DD' format.
            end_date (str): The end date of the tournament in 'YYYY-MM-DD' format.
            time_control (TimeControl): The time control of the tournament.
        """
        super().__init__(name, location, start_date, end_date, time_control)