from src.views import MainView


def main():
    """Entry point for the chess tournament management system."""
    app = MainView()
    app.run()


if __name__ == "__main__":
    main()