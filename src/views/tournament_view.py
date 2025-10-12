from .base_view import BaseView


class TournamentView(BaseView):
    """View class for managing tournament-related screens."""

    def __init__(self):
        # TODO: Inicializar o controller de torneio quando estiver disponível
        pass

    def show_menu(self):
        """Display the tournament menu and handle user input."""
        while True:
            self.clear_screen()
            self.display_separator()
            print("           MENU DE TORNEIOS")
            self.display_separator()
            print("1 - Criar novo torneio")
            print("2 - Listar torneios")
            print("3 - Gerenciar torneio")
            print("4 - Voltar ao menu principal")
            self.display_separator()

            choice = self.get_input("\nEscolha uma opção: ")

            if choice == '1':
                self.create_tournament_screen()
            elif choice == '2':
                self.list_tournaments_screen()
            elif choice == '3':
                self.manage_tournament_screen()
            elif choice == '4':
                break
            else:
                self.display_error("Opção inválida!")
                self.pause()

    def create_tournament_screen(self):
        """Screen for creating a new tournament."""
        self.clear_screen()
        self.display_separator()
        print("           CRIAR NOVO TORNEIO")
        self.display_separator()
        
        # TODO: Implementar quando o controller de torneio estiver pronto
        self.display_message("\n⚠️  Funcionalidade em desenvolvimento")
        self.pause()

    def list_tournaments_screen(self):
        """Screen for listing all tournaments."""
        self.clear_screen()
        self.display_separator()
        print("           LISTA DE TORNEIOS")
        self.display_separator()
        
        # TODO: Implementar quando o controller de torneio estiver pronto
        self.display_message("\n⚠️  Funcionalidade em desenvolvimento")
        self.pause()

    def manage_tournament_screen(self):
        """Screen for managing a specific tournament."""
        self.clear_screen()
        self.display_separator()
        print("           GERENCIAR TORNEIO")
        self.display_separator()
        
        # TODO: Implementar quando o controller de torneio estiver pronto
        self.display_message("\n⚠️  Funcionalidade em desenvolvimento")
        self.pause()
