from src.entities.tournament import Tournament

from src.utils.decorators import type_check

class EliminatoryTournament(Tournament):
    """Class representing an eliminatory chess tournament."""
    @type_check
    def __init__(self, name: str, location: str, start_date: str, end_date: str):
        """
        Initialize an EliminatoryTournament instance.

        Args:
            name (str): The name of the tournament.
            location (str): The location of the tournament.
            start_date (str): The start date of the tournament in 'YYYY-MM-DD' format.
            end_date (str): The end date of the tournament in 'YYYY-MM-DD' format.
        """
        super().__init__(name, location, start_date, end_date)