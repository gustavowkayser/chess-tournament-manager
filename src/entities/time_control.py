from enum import Enum


class TimeControl(Enum):
    """Enum representing different time controls for chess tournaments."""
    CLASSIC = "classic"
    RAPID = "rapid"
    BLITZ = "blitz"

    def __str__(self):
        """Return a user-friendly string representation."""
        names = {
            "classic": "Clássico",
            "rapid": "Rápido",
            "blitz": "Blitz"
        }
        return names.get(self.value, self.value)

    @staticmethod
    def from_string(value: str) -> 'TimeControl':
        """
        Create a TimeControl from a string value.

        Args:
            value (str): The string value ('classic', 'rapid', or 'blitz').

        Returns:
            TimeControl: The corresponding TimeControl enum.

        Raises:
            ValueError: If the value is not valid.
        """
        value_lower = value.lower()
        for time_control in TimeControl:
            if time_control.value == value_lower:
                return time_control
        raise ValueError(f"Invalid time control: {value}. Must be 'classic', 'rapid', or 'blitz'.")
