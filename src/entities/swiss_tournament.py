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
        self.__num_rounds = rounds  # Number of rounds in the Swiss tournament

    @property
    def num_rounds(self) -> int:
        """Get the number of rounds in the Swiss tournament."""
        return self.__num_rounds
    
    @num_rounds.setter
    def num_rounds(self, value: int):
        """Set the number of rounds in the Swiss tournament."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Number of rounds must be a positive integer.")
        self.__num_rounds = value

    def generate_swiss_pairings(self, round_number: int) -> list:
        """
        Generate pairings for a Swiss tournament round.

        Args:
            round_number (int): The round number to generate pairings for.

        Returns:
            list: List of tuples (white_player, black_player) representing the pairings.

        Raises:
            ValueError: If there are insufficient players or round number is invalid.
        """
        from src.entities.game import Game
        import random

        players = self.players
        
        if len(players) < 2:
            raise ValueError("At least 2 players are required to generate pairings.")

        if round_number <= 0 or round_number > self.__num_rounds:
            raise ValueError(f"Round number must be between 1 and {self.__num_rounds}.")

        # For the first round, pair by rating
        if round_number == 1:
            # Sort players by rating (using tournament's time control)
            rating_type = self.time_control.value
            sorted_players = sorted(
                players,
                key=lambda p: getattr(p.rating, rating_type),
                reverse=True
            )
            
            # Split into top and bottom halves and pair
            mid = len(sorted_players) // 2
            top_half = sorted_players[:mid]
            bottom_half = sorted_players[mid:]
            
            pairings = []
            for i in range(min(len(top_half), len(bottom_half))):
                # Alternate colors: odd rounds top half gets white
                if round_number % 2 == 1:
                    pairings.append((top_half[i], bottom_half[i]))
                else:
                    pairings.append((bottom_half[i], top_half[i]))
            
            # If odd number of players, one gets a bye
            if len(sorted_players) % 2 == 1:
                pairings.append((sorted_players[-1], None))  # Bye
            
            return pairings
        
        # For subsequent rounds, use a simple Swiss pairing algorithm
        # In a real implementation, this would consider previous opponents and color balance
        else:
            # Get scores from previous rounds (simplified - would need to track actual scores)
            rating_type = self.time_control.value
            sorted_players = sorted(
                players,
                key=lambda p: getattr(p.rating, rating_type),
                reverse=True
            )
            
            # Simple pairing: pair consecutive players
            pairings = []
            paired = set()
            
            for i in range(0, len(sorted_players) - 1, 2):
                if sorted_players[i].name not in paired and sorted_players[i+1].name not in paired:
                    # Alternate colors based on round number
                    if round_number % 2 == 1:
                        pairings.append((sorted_players[i], sorted_players[i+1]))
                    else:
                        pairings.append((sorted_players[i+1], sorted_players[i]))
                    paired.add(sorted_players[i].name)
                    paired.add(sorted_players[i+1].name)
            
            # Handle bye if odd number of players
            if len(sorted_players) % 2 == 1:
                unpaired = [p for p in sorted_players if p.name not in paired]
                if unpaired:
                    pairings.append((unpaired[0], None))
            
            return pairings
