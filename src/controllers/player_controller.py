from .base_controller import BaseController
from src.entities.player import Player
from src.dtos.player_dto import PlayerDTO

class PlayerController(BaseController):
    """Controller for managing player-related operations."""

    def __init__(self):
        super().__init__()
        self.filename = 'players.json'

    def register_player(self, player: Player):
        """
        Register a new player.

        Args:
            player (Player): The player object to register.
        """
        player_data = PlayerDTO.to_dict(player)
        players = self._load_data()
        if not isinstance(players, list):
            raise ValueError("Invalid data format.")
        if player_data.get('name') in [player.get('name') for player in players]:
            raise ValueError("Player with this name already exists.")

        players.append(player_data)
        self._save_data(players)

    def get_all_players(self) -> list:
        """
        Retrieve all registered players.

        Returns:
            list: A list of dictionaries, each representing a player.
        """
        all_players = self._load_data()
        if not isinstance(all_players, list):
            raise ValueError("Invalid data format.")
        return [PlayerDTO.from_dict(player) for player in all_players]