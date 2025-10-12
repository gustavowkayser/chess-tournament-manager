from src.entities.tournament import Tournament
from src.entities.swiss_tournament import SwissTournament
from src.entities.eliminatory_tournament import EliminatoryTournament
from src.entities.time_control import TimeControl
from src.entities.round import Round
from src.entities.game import Game
from src.dtos.player_dto import PlayerDTO


class TournamentDTO:
    """Data Transfer Object for Tournament entities."""

    @staticmethod
    def _game_to_dict(game: Game) -> dict:
        """
        Convert a Game object to a dictionary.

        Args:
            game (Game): The game object to convert.

        Returns:
            dict: Dictionary representation of the game.
        """
        return {
            "white": PlayerDTO.to_dict(game.white),
            "black": PlayerDTO.to_dict(game.black) if game.black else None,
            "result": game.result
        }

    @staticmethod
    def _game_from_dict(data: dict) -> Game:
        """
        Create a Game object from a dictionary.

        Args:
            data (dict): Dictionary containing game data.

        Returns:
            Game: The created game object.
        """
        white = PlayerDTO.from_dict(data["white"])
        black = PlayerDTO.from_dict(data["black"]) if data["black"] else None
        game = Game(white, black)
        if data.get("result"):
            game.result = data["result"]
        return game

    @staticmethod
    def _round_to_dict(round_obj: Round) -> dict:
        """
        Convert a Round object to a dictionary.

        Args:
            round_obj (Round): The round object to convert.

        Returns:
            dict: Dictionary representation of the round.
        """
        return {
            "round_number": round_obj.round_,
            "subround": round_obj.subround,
            "matches": [TournamentDTO._game_to_dict(game) for game in round_obj.matches]
        }

    @staticmethod
    def _round_from_dict(data: dict) -> Round:
        """
        Create a Round object from a dictionary.

        Args:
            data (dict): Dictionary containing round data.

        Returns:
            Round: The created round object.
        """
        round_obj = Round(data["round_number"], data.get("subround", 0))
        matches_data = data.get("matches", [])
        for match_data in matches_data:
            game = TournamentDTO._game_from_dict(match_data)
            round_obj.add_match(game)
        return round_obj

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
            "time_control": tournament.time_control.value,
            "players": [PlayerDTO.to_dict(player) for player in tournament.players],
            "rounds_data": [TournamentDTO._round_to_dict(round_obj) for round_obj in tournament.rounds]
        }

        # Add type-specific information
        if isinstance(tournament, SwissTournament):
            data["type"] = "swiss"
            data["num_rounds"] = tournament.num_rounds
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
        time_control_str = data.get("time_control", "classic")
        time_control = TimeControl.from_string(time_control_str)

        # Create tournament based on type
        if tournament_type == "swiss":
            num_rounds = data.get("num_rounds", 0)
            tournament = SwissTournament(name, location, start_date, end_date, time_control, num_rounds)
        elif tournament_type == "eliminatory":
            tournament = EliminatoryTournament(name, location, start_date, end_date, time_control)
        else:
            tournament = Tournament(name, location, start_date, end_date, time_control)

        # Add players to tournament
        players_data = data.get("players", [])
        for player_data in players_data:
            player = PlayerDTO.from_dict(player_data)
            tournament.add_player(player)

        # Add rounds to tournament
        rounds_data = data.get("rounds_data", [])
        for round_data in rounds_data:
            round_obj = TournamentDTO._round_from_dict(round_data)
            tournament.add_round(round_obj)

        return tournament

