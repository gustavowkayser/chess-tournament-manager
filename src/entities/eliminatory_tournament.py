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

    def generate_bracket_pairings(self, round_number: int) -> list:
        """
        Generate bracket pairings for an eliminatory tournament.

        Args:
            round_number (int): The round number (1 = first round, 2 = semifinals, etc.).

        Returns:
            list: List of tuples (white_player, black_player) representing the pairings.

        Raises:
            ValueError: If there are insufficient players or invalid round.
        """
        import math

        players = self.players
        num_players = len(players)

        if num_players < 2:
            raise ValueError("At least 2 players are required for an eliminatory tournament.")

        # Calculate maximum rounds based on number of players
        max_rounds = math.ceil(math.log2(num_players))

        if round_number <= 0 or round_number > max_rounds:
            raise ValueError(f"Invalid round number. Must be between 1 and {max_rounds}.")

        # For first round, seed players by rating
        if round_number == 1:
            rating_type = self.time_control.value
            sorted_players = sorted(
                players,
                key=lambda p: getattr(p.rating, rating_type),
                reverse=True
            )

            # Calculate number of players for first round
            # If not power of 2, some players get byes
            next_power_of_2 = 2 ** math.ceil(math.log2(num_players))
            num_byes = next_power_of_2 - num_players

            pairings = []
            
            # Top seeds get byes if needed
            bye_players = sorted_players[:num_byes] if num_byes > 0 else []
            active_players = sorted_players[num_byes:] if num_byes > 0 else sorted_players

            # Pair remaining players (1 vs last, 2 vs second-last, etc.)
            for i in range(len(active_players) // 2):
                white = active_players[i]
                black = active_players[-(i + 1)]
                pairings.append((white, black))

            # Add byes as special pairings
            for bye_player in bye_players:
                pairings.append((bye_player, None))  # Bye - automatic advance

            return pairings

        # For subsequent rounds, pair winners from previous round
        else:
            # Get the previous round
            previous_round = self.get_round(round_number - 1)
            
            if previous_round is None:
                raise ValueError(f"Previous round (round {round_number - 1}) must be completed before generating round {round_number}.")
            
            # Get winners from previous round
            winners = []
            for match in previous_round.matches:
                winner = self._get_match_winner(match)
                if winner is None:
                    raise ValueError(f"All matches in round {round_number - 1} must have results before generating next round.")
                winners.append(winner)
            
            if len(winners) < 2:
                raise ValueError("At least 2 winners are required to generate next round.")
            
            # Pair winners sequentially (winner of match 1 vs winner of match 2, etc.)
            pairings = []
            for i in range(0, len(winners) - 1, 2):
                pairings.append((winners[i], winners[i + 1]))
            
            return pairings

    def _get_match_winner(self, match):
        """
        Determine the winner of a match based on the result.
        
        Args:
            match: The Game object representing the match.
            
        Returns:
            Player: The winning player, or None if no result.
        """
        # If it's a BYE, white advances automatically
        if match.black is None:
            return match.white
        
        # If no result, can't determine winner
        if match.result is None:
            return None
        
        # Parse the result to determine winner
        # Result format: "X-Y" where X is white's score and Y is black's score
        try:
            parts = match.result.split('-')
            if len(parts) != 2:
                return None
            
            white_score = float(parts[0])
            black_score = float(parts[1])
            
            if white_score > black_score:
                return match.white
            elif black_score > white_score:
                return match.black
            else:
                # Tie - should not happen in eliminatory, but return None
                return None
        except (ValueError, AttributeError):
            return None

    def get_bracket_info(self) -> dict:
        """
        Get information about the tournament bracket structure.

        Returns:
            dict: Information about rounds and structure.
        """
        import math

        num_players = len(self.players)
        if num_players < 2:
            return {
                "total_rounds": 0,
                "structure": "Insufficient players"
            }

        total_rounds = math.ceil(math.log2(num_players))
        next_power_of_2 = 2 ** math.ceil(math.log2(num_players))
        num_byes = next_power_of_2 - num_players

        round_names = {
            1: "Primeira Rodada",
            2: "Oitavas de Final" if total_rounds >= 4 else "Semifinal",
            3: "Quartas de Final" if total_rounds >= 4 else "Final",
            4: "Semifinal",
            5: "Final"
        }

        # Adjust for actual number of rounds
        if total_rounds == 1:
            round_names[1] = "Final"
        elif total_rounds == 2:
            round_names = {1: "Semifinal", 2: "Final"}
        elif total_rounds == 3:
            round_names = {1: "Quartas de Final", 2: "Semifinal", 3: "Final"}

        return {
            "total_rounds": total_rounds,
            "num_players": num_players,
            "bracket_size": next_power_of_2,
            "byes_in_first_round": num_byes,
            "round_names": {i: round_names.get(i, f"Rodada {i}") for i in range(1, total_rounds + 1)}
        }
