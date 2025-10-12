class BaseView:
    """Base class for all views in the system."""

    @staticmethod
    def clear_screen():
        """Clear the console screen."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def display_message(message: str):
        """
        Display a message to the user.

        Args:
            message (str): The message to display.
        """
        print(message)

    @staticmethod
    def display_error(error: str):
        """
        Display an error message to the user.

        Args:
            error (str): The error message to display.
        """
        print(f"\n❌ Erro: {error}\n")

    @staticmethod
    def display_success(message: str):
        """
        Display a success message to the user.

        Args:
            message (str): The success message to display.
        """
        print(f"\n✅ {message}\n")

    @staticmethod
    def get_input(prompt: str) -> str:
        """
        Get input from the user.

        Args:
            prompt (str): The prompt to display to the user.

        Returns:
            str: The user's input.
        """
        return input(prompt)

    @staticmethod
    def display_separator():
        """Display a separator line."""
        print("=" * 60)

    @staticmethod
    def pause():
        """Pause execution until user presses Enter."""
        input("\nPressione Enter para continuar...")
