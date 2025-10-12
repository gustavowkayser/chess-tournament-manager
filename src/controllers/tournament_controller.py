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

    def generate_round_pairings(self, tournament_name: str) -> tuple:
        """
        Generate pairings for the next round of a tournament.

        Args:
            tournament_name (str): The name of the tournament.

        Returns:
            tuple: (round_number, pairings_list, tournament_object)

        Raises:
            ValueError: If tournament is not found or pairings cannot be generated.
        """
        tournament = self.get_tournament_by_name(tournament_name)
        
        if tournament is None:
            raise ValueError(f"Tournament '{tournament_name}' not found.")
        
        if len(tournament.players) < 2:
            raise ValueError("At least 2 players are required to generate pairings.")
        
        round_number = tournament.get_current_round_number()
        
        # Generate pairings based on tournament type
        if isinstance(tournament, SwissTournament):
            if round_number > tournament.num_rounds:
                raise ValueError(f"Tournament has only {tournament.num_rounds} rounds. All rounds completed.")
            pairings = tournament.generate_swiss_pairings(round_number)
        elif isinstance(tournament, EliminatoryTournament):
            bracket_info = tournament.get_bracket_info()
            if round_number > bracket_info['total_rounds']:
                raise ValueError(f"Tournament bracket complete. All {bracket_info['total_rounds']} rounds finished.")
            pairings = tournament.generate_bracket_pairings(round_number)
        else:
            raise ValueError("Pairing generation not supported for basic tournaments.")
        
        return (round_number, pairings, tournament)

    def save_round_pairings(self, tournament_name: str, round_number: int, pairings: list) -> None:
        """
        Save the pairings for a round to the tournament.

        Args:
            tournament_name (str): The name of the tournament.
            round_number (int): The round number.
            pairings (list): List of tuples (white_player, black_player).

        Raises:
            ValueError: If tournament is not found or save fails.
        """
        from src.entities.round import Round
        from src.entities.game import Game
        
        tournament = self.get_tournament_by_name(tournament_name)
        
        if tournament is None:
            raise ValueError(f"Tournament '{tournament_name}' not found.")
        
        # Create Round object
        round_obj = Round(round_number)
        
        # Add games to round
        for white, black in pairings:
            if black is None:
                # Bye - create a game with None as black player
                game = Game(white, white)  # Using same player as placeholder for bye
                game.result = "1-0"  # Bye automatically wins
            else:
                game = Game(white, black)
            round_obj.add_match(game)
        
        # Add round to tournament
        tournament.add_round(round_obj)
        
        # Save updated tournament
        self.update_tournament(tournament_name, tournament)

    def get_bracket_info(self, tournament_name: str) -> dict:
        """
        Get bracket information for an eliminatory tournament.

        Args:
            tournament_name (str): The name of the tournament.

        Returns:
            dict: Bracket information.

        Raises:
            ValueError: If tournament is not found or not eliminatory.
        """
        tournament = self.get_tournament_by_name(tournament_name)
        
        if tournament is None:
            raise ValueError(f"Tournament '{tournament_name}' not found.")
        
        if not isinstance(tournament, EliminatoryTournament):
            raise ValueError("Bracket information is only available for eliminatory tournaments.")
        
        return tournament.get_bracket_info()

    def get_round_matches(self, tournament_name: str, round_number: int) -> list:
        """
        Get all matches from a specific round.

        Args:
            tournament_name (str): The name of the tournament.
            round_number (int): The round number.

        Returns:
            list: List of Game objects from the round.

        Raises:
            ValueError: If tournament or round is not found.
        """
        tournament = self.get_tournament_by_name(tournament_name)
        
        if tournament is None:
            raise ValueError(f"Tournament '{tournament_name}' not found.")
        
        round_obj = tournament.get_round(round_number)
        
        if round_obj is None:
            raise ValueError(f"Round {round_number} not found in tournament.")
        
        return round_obj.matches

    def update_match_result(self, tournament_name: str, round_number: int, match_index: int, result: str) -> None:
        """
        Update the result of a specific match.

        Args:
            tournament_name (str): The name of the tournament.
            round_number (int): The round number.
            match_index (int): The index of the match in the round.
            result (str): The result ('1-0', '0-1', or '0.5-0.5').

        Raises:
            ValueError: If tournament, round, or match is not found.
        """
        tournament = self.get_tournament_by_name(tournament_name)
        
        if tournament is None:
            raise ValueError(f"Tournament '{tournament_name}' not found.")
        
        round_obj = tournament.get_round(round_number)
        
        if round_obj is None:
            raise ValueError(f"Round {round_number} not found in tournament.")
        
        if match_index < 0 or match_index >= len(round_obj.matches):
            raise ValueError(f"Match index {match_index} out of range.")
        
        # Update the result
        round_obj.matches[match_index].result = result
        
        # Save updated tournament
        self.update_tournament(tournament_name, tournament)

    def get_player_statistics(self, tournament_name: str, player_name: str) -> dict:
        """
        Get statistics for a specific player in a tournament.
        
        Args:
            tournament_name (str): The name of the tournament.
            player_name (str): The name of the player.
            
        Returns:
            dict: Dictionary with player statistics including:
                - points: Total points scored
                - games_played: Number of games played
                - wins: Number of wins
                - draws: Number of draws
                - losses: Number of losses
                - opponents_ratings: List of opponent ratings
                - average_opponent_rating: Average rating of opponents
                - performance_rating: Calculated performance rating
                
        Raises:
            ValueError: If tournament or player not found.
        """
        tournament = self.get_tournament_by_name(tournament_name)
        
        if tournament is None:
            raise ValueError(f"Tournament '{tournament_name}' not found.")
        
        # Find the player
        player = None
        for p in tournament.players:
            if p.name == player_name:
                player = p
                break
        
        if player is None:
            raise ValueError(f"Player '{player_name}' not found in tournament.")
        
        # Get rating type based on time control
        rating_type = tournament.time_control.value
        player_rating = getattr(player.rating, rating_type)
        
        # Initialize statistics
        stats = {
            'points': 0.0,
            'games_played': 0,
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'opponents_ratings': [],
            'average_opponent_rating': 0,
            'performance_rating': 0,
            'rating_change': 0
        }
        
        # Go through all rounds and matches
        for round_obj in tournament.rounds:
            for match in round_obj.matches:
                # Check if player is in this match
                is_white = match.white.name == player_name
                is_black = match.black and match.black.name == player_name
                
                if not (is_white or is_black):
                    continue
                
                # If opponent is None (BYE), count as win
                if match.black is None and is_white:
                    stats['points'] += 1.0
                    stats['wins'] += 1
                    stats['games_played'] += 1
                    continue
                
                # Get opponent and their rating
                opponent = match.black if is_white else match.white
                opponent_rating = getattr(opponent.rating, rating_type)
                stats['opponents_ratings'].append(opponent_rating)
                
                # If no result yet, skip
                if match.result is None:
                    continue
                
                stats['games_played'] += 1
                
                # Parse result
                try:
                    parts = match.result.split('-')
                    if len(parts) == 2:
                        white_score = float(parts[0])
                        black_score = float(parts[1])
                        
                        player_score = white_score if is_white else black_score
                        stats['points'] += player_score

                        # Calculate rating change
                        qA = 10 ** (player_rating / 400)
                        qB = 10 ** (opponent_rating / 400)
                        eA = qA / (qA + qB)
                        k = 20  # K-factor, can be adjusted
                        rating_change = k * (player_score - eA)
                        stats['rating_change'] += rating_change
                        
                        # Determine win/draw/loss (for single games)
                        if white_score == 1.0 and black_score == 0.0:
                            if is_white:
                                stats['wins'] += 1
                            else:
                                stats['losses'] += 1
                        elif white_score == 0.0 and black_score == 1.0:
                            if is_black:
                                stats['wins'] += 1
                            else:
                                stats['losses'] += 1
                        elif white_score == 0.5 and black_score == 0.5:
                            stats['draws'] += 1
                except (ValueError, AttributeError):
                    pass
        
        # Calculate average opponent rating
        if stats['opponents_ratings']:
            stats['average_opponent_rating'] = sum(stats['opponents_ratings']) / len(stats['opponents_ratings'])
        
        # Calculate performance rating
        if stats['games_played'] > 0:
            percentage = stats['points'] / stats['games_played']
            
            # Using simplified performance rating calculation
            # Performance = Average Opponent Rating + 400 * (W - L) / N
            # Or using percentage: Performance = Avg Opp Rating + dp
            # Where dp comes from percentage score table
            
            if percentage == 1.0:
                # 100% score
                stats['performance_rating'] = int(stats['average_opponent_rating'] + 400)
            elif percentage == 0.0:
                # 0% score
                stats['performance_rating'] = int(stats['average_opponent_rating'] - 400)
            else:
                # Use simplified formula: dp ≈ -400 * log10((1-p)/p)
                import math
                try:
                    dp = -400 * math.log10((1 - percentage) / percentage)
                    stats['performance_rating'] = int(stats['average_opponent_rating'] + dp)
                except (ValueError, ZeroDivisionError):
                    stats['performance_rating'] = int(stats['average_opponent_rating'])


        
        return stats

    def get_all_players_statistics(self, tournament_name: str) -> list:
        """
        Get statistics for all players in a tournament.
        
        Args:
            tournament_name (str): The name of the tournament.
            
        Returns:
            list: List of tuples (player, statistics_dict).
        """
        tournament = self.get_tournament_by_name(tournament_name)
        
        if tournament is None:
            raise ValueError(f"Tournament '{tournament_name}' not found.")
        
        results = []
        for player in tournament.players:
            stats = self.get_player_statistics(tournament_name, player.name)
            results.append((player, stats))
        
        return results






