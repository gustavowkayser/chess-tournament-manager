import json

class BaseController:
    """Base controller class providing common functionalities for all controllers."""

    def __init__(self):
        self.data_path = 'src/data/'
        self.filename = ''

    def _load_data(self, filename: str | None = None) -> dict | list:
        """Load data from a JSON file."""
        filename = filename or self.filename
        try:
            with open(self.data_path + filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from file: {filename}")

    def _save_data(self, data: dict | list, filename: str | None = None) -> None:
        """Save data to a JSON file."""
        filename = filename or self.filename
        with open(self.data_path + filename, 'w') as file:
            json.dump(data, file, indent=4)
