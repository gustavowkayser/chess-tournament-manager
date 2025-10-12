from .base_controller import BaseController
from src.entities.tournament import Tournament
from src.entities.swiss_tournament import SwissTournament
from src.entities.eliminatory_tournament import EliminatoryTournament
from src.dtos.tournament_dto import TournamentDTO


class TournamentController(BaseController):
    """Controller for managing tournament-related operations."""

    def __init__(self):
        super().__init__()
        self.filename = 'tournaments.json'

    def create_tournament(self, tournament: Tournament) -> None:
        """
        Create a new tournament.

        Args:
            tournament (Tournament): The tournament object to create.

        Raises:
            ValueError: If tournament with same name already exists or data format is invalid.
        """
        tournament_data = TournamentDTO.to_dict(tournament)
        tournaments = self._load_data()
        
        if not isinstance(tournaments, list):
            raise ValueError("Invalid data format.")
        
        # Check if tournament with same name already exists
        if tournament_data.get('name') in [t.get('name') for t in tournaments]:
            raise ValueError("Tournament with this name already exists.")

        tournaments.append(tournament_data)
        self._save_data(tournaments)

    def get_all_tournaments(self) -> list:
        """
        Retrieve all registered tournaments.

        Returns:
            list: A list of Tournament objects.

        Raises:
            ValueError: If data format is invalid.
        """
        all_tournaments = self._load_data()
        
        if not isinstance(all_tournaments, list):
            raise ValueError("Invalid data format.")
        
        return [TournamentDTO.from_dict(tournament) for tournament in all_tournaments]

    def get_tournament_by_name(self, name: str) -> Tournament | None:
        """
        Retrieve a tournament by its name.

        Args:
            name (str): The name of the tournament to retrieve.

        Returns:
            Tournament | None: The tournament object if found, None otherwise.
        """
        tournaments = self._load_data()
        
        if not isinstance(tournaments, list):
            raise ValueError("Invalid data format.")
        
        for tournament_data in tournaments:
            if tournament_data.get('name') == name:
                return TournamentDTO.from_dict(tournament_data)
        
        return None

    def update_tournament(self, old_name: str, tournament: Tournament) -> None:
        """
        Update an existing tournament.

        Args:
            old_name (str): The current name of the tournament to update.
            tournament (Tournament): The updated tournament object.

        Raises:
            ValueError: If tournament is not found or data format is invalid.
        """
        tournaments = self._load_data()
        
        if not isinstance(tournaments, list):
            raise ValueError("Invalid data format.")
        
        # Find and update the tournament
        updated = False
        for i, tournament_data in enumerate(tournaments):
            if tournament_data.get('name') == old_name:
                tournaments[i] = TournamentDTO.to_dict(tournament)
                updated = True
                break
        
        if not updated:
            raise ValueError(f"Tournament '{old_name}' not found.")
        
        self._save_data(tournaments)

    def delete_tournament(self, name: str) -> None:
        """
        Delete a tournament by its name.

        Args:
            name (str): The name of the tournament to delete.

        Raises:
            ValueError: If tournament is not found or data format is invalid.
        """
        tournaments = self._load_data()
        
        if not isinstance(tournaments, list):
            raise ValueError("Invalid data format.")
        
        # Find and remove the tournament
        initial_length = len(tournaments)
        tournaments = [t for t in tournaments if t.get('name') != name]
        
        if len(tournaments) == initial_length:
            raise ValueError(f"Tournament '{name}' not found.")
        
        self._save_data(tournaments)

    def get_tournaments_by_type(self, tournament_type: str) -> list:
        """
        Retrieve tournaments by type.

        Args:
            tournament_type (str): The type of tournament ('swiss', 'eliminatory', or 'basic').

        Returns:
            list: A list of Tournament objects of the specified type.
        """
        all_tournaments = self._load_data()
        
        if not isinstance(all_tournaments, list):
            raise ValueError("Invalid data format.")
        
        filtered_tournaments = [
            TournamentDTO.from_dict(t) for t in all_tournaments 
            if t.get('type') == tournament_type
        ]
        
        return filtered_tournaments

    def add_player_to_tournament(self, tournament_name: str, player) -> None:
        """
        Add a player to a tournament.

        Args:
            tournament_name (str): The name of the tournament.
            player: The player object to add.

        Raises:
            ValueError: If tournament is not found or player cannot be added.
        """
        tournament = self.get_tournament_by_name(tournament_name)
        
        if tournament is None:
            raise ValueError(f"Tournament '{tournament_name}' not found.")
        
        tournament.add_player(player)
        self.update_tournament(tournament_name, tournament)

    def remove_player_from_tournament(self, tournament_name: str, player_name: str) -> None:
        """
        Remove a player from a tournament.

        Args:
            tournament_name (str): The name of the tournament.
            player_name (str): The name of the player to remove.

        Raises:
            ValueError: If tournament or player is not found.
        """
        tournament = self.get_tournament_by_name(tournament_name)
        
        if tournament is None:
            raise ValueError(f"Tournament '{tournament_name}' not found.")
        
        tournament.remove_player(player_name)
        self.update_tournament(tournament_name, tournament)

    def get_tournament_ranking(self, tournament_name: str, rating_type: str = 'classic') -> list:
        """
        Get the ranking of players in a tournament based on rating.

        Args:
            tournament_name (str): The name of the tournament.
            rating_type (str): The type of rating to use ('classic', 'rapid', or 'blitz').

        Returns:
            list: List of players sorted by rating (highest to lowest).

        Raises:
            ValueError: If tournament is not found.
        """
        tournament = self.get_tournament_by_name(tournament_name)
        
        if tournament is None:
            raise ValueError(f"Tournament '{tournament_name}' not found.")
        
        return tournament.get_players_by_rating(rating_type)

