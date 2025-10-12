from .base_view import BaseView
from .player_view import PlayerView
from .tournament_view import TournamentView


class MainView(BaseView):
    """Main view class for the chess tournament management system."""

    def __init__(self):
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()

    def show_main_menu(self):
        """Display the main menu and handle user navigation."""
        while True:
            self.clear_screen()
            self.display_separator()
            print("    SISTEMA DE GERENCIAMENTO DE TORNEIOS DE XADREZ")
            self.display_separator()
            print("1 - Jogador")
            print("2 - Torneio")
            print("3 - Sair")
            self.display_separator()

            choice = self.get_input("\nEscolha uma opção: ")

            if choice == '1':
                self.player_view.show_menu()
            elif choice == '2':
                self.tournament_view.show_menu()
            elif choice == '3':
                self.clear_screen()
                self.display_success("Encerrando o sistema. Até logo!")
                break
            else:
                self.display_error("Opção inválida!")
                self.pause()

    def run(self):
        """Start the application."""
        self.show_main_menu()
