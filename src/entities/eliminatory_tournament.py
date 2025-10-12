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
        # This would require tracking match results
        else:
            # Simplified: get players who should still be in tournament
            # In real implementation, this would filter based on previous round winners
            rating_type = self.time_control.value
            sorted_players = sorted(
                players,
                key=lambda p: getattr(p.rating, rating_type),
                reverse=True
            )

            # Calculate expected number of players for this round
            expected_players = max(2, 2 ** (max_rounds - round_number + 1))
            active_players = sorted_players[:min(expected_players, len(sorted_players))]

            pairings = []
            for i in range(0, len(active_players) - 1, 2):
                pairings.append((active_players[i], active_players[i + 1]))

            return pairings

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
