from .base_view import BaseView
from src.controllers.player_controller import PlayerController
from src.entities.player import Player
from src.entities.rating import Rating


class PlayerView(BaseView):
    """View class for managing player-related screens."""

    def __init__(self):
        self.controller = PlayerController()

    def show_menu(self):
        """Display the player menu and handle user input."""
        while True:
            self.clear_screen()
            self.display_separator()
            print("           MENU DE JOGADORES")
            self.display_separator()
            print("1 - Registrar novo jogador")
            print("2 - Listar todos os jogadores")
            print("3 - Voltar ao menu principal")
            self.display_separator()

            choice = self.get_input("\nEscolha uma opção: ")

            if choice == '1':
                self.register_player_screen()
            elif choice == '2':
                self.list_players_screen()
            elif choice == '3':
                break
            else:
                self.display_error("Opção inválida!")
                self.pause()

    def register_player_screen(self):
        """Screen for registering a new player."""
        self.clear_screen()
        self.display_separator()
        print("           REGISTRAR NOVO JOGADOR")
        self.display_separator()

        try:
            name = self.get_input("\nNome do jogador: ")
            birthdate = self.get_input("Data de nascimento (YYYY-MM-DD): ")
            gender = self.get_input("Gênero: ")
            
            print("\nRatings do jogador:")
            classic_rating = int(self.get_input("  Rating Clássico: "))
            rapid_rating = int(self.get_input("  Rating Rápido: "))
            blitz_rating = int(self.get_input("  Rating Blitz: "))

            rating = Rating(classic_rating, rapid_rating, blitz_rating)
            player = Player(name, birthdate, gender, rating)
            
            self.controller.register_player(player)
            self.display_success(f"Jogador '{name}' registrado com sucesso!")
        except ValueError as e:
            self.display_error(str(e))
        except Exception as e:
            self.display_error(f"Erro ao registrar jogador: {str(e)}")

        self.pause()

    def list_players_screen(self):
        """Screen for listing all registered players."""
        self.clear_screen()
        self.display_separator()
        print("           LISTA DE JOGADORES")
        self.display_separator()

        try:
            players = self.controller.get_all_players()
            
            if not players:
                print("\nNenhum jogador registrado ainda.")
            else:
                print(f"\nTotal de jogadores: {len(players)}\n")
                for i, player in enumerate(players, 1):
                    print(f"{i}. {player.name}")
                    print(f"   Data de Nascimento: {player.birthdate}")
                    print(f"   Gênero: {player.gender}")
                    print(f"   Ratings:")
                    print(f"     - Clássico: {player.rating.classic}")
                    print(f"     - Rápido: {player.rating.rapid}")
                    print(f"     - Blitz: {player.rating.blitz}")
                    print()
        except Exception as e:
            self.display_error(f"Erro ao listar jogadores: {str(e)}")

        self.pause()
