from src.entities.tournament import Tournament
from src.entities.swiss_tournament import SwissTournament
from src.entities.eliminatory_tournament import EliminatoryTournament


class TournamentDTO:
    """Data Transfer Object for Tournament entities."""

    @staticmethod
    def to_dict(tournament: Tournament) -> dict:
        """
        Convert a Tournament object to a dictionary.

        Args:
            tournament (Tournament): The tournament object to convert.

        Returns:
            dict: Dictionary representation of the tournament.
        """
        data = {
            "name": tournament.name,
            "location": tournament.location,
            "start_date": tournament.start_date,
            "end_date": tournament.end_date,
        }

        # Add type-specific information
        if isinstance(tournament, SwissTournament):
            data["type"] = "swiss"
            data["rounds"] = tournament.rounds
        elif isinstance(tournament, EliminatoryTournament):
            data["type"] = "eliminatory"
        else:
            data["type"] = "basic"

        return data

    @staticmethod
    def from_dict(data: dict) -> Tournament:
        """
        Create a Tournament object from a dictionary.

        Args:
            data (dict): Dictionary containing tournament data.

        Returns:
            Tournament: The created tournament object.
        """
        tournament_type = data.get("type", "basic")
        name = data.get("name", "")
        location = data.get("location", "")
        start_date = data.get("start_date", "")
        end_date = data.get("end_date", "")

        if tournament_type == "swiss":
            rounds = data.get("rounds", 5)
            return SwissTournament(name, location, start_date, end_date, rounds)
        elif tournament_type == "eliminatory":
            return EliminatoryTournament(name, location, start_date, end_date)
        else:
            return Tournament(name, location, start_date, end_date)
