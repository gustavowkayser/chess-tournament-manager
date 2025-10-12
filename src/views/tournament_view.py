from .base_view import BaseView
from src.controllers.tournament_controller import TournamentController
from src.controllers.player_controller import PlayerController
from src.entities.swiss_tournament import SwissTournament
from src.entities.eliminatory_tournament import EliminatoryTournament


class TournamentView(BaseView):
    """View class for managing tournament-related screens."""

    def __init__(self):
        self.controller = TournamentController()
        self.player_controller = PlayerController()

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

        try:
            # Get basic tournament information
            name = self.get_input("\nNome do torneio: ")
            location = self.get_input("Local: ")
            start_date = self.get_input("Data de início (YYYY-MM-DD): ")
            end_date = self.get_input("Data de término (YYYY-MM-DD): ")

            # Select tournament type
            print("\nTipo de torneio:")
            print("1 - Torneio Suíço")
            print("2 - Torneio Eliminatório")
            tournament_type = self.get_input("\nEscolha o tipo: ")

            if tournament_type == '1':
                # Swiss tournament
                rounds = int(self.get_input("Número de rodadas: "))
                tournament = SwissTournament(name, location, start_date, end_date, rounds)
            elif tournament_type == '2':
                # Eliminatory tournament
                tournament = EliminatoryTournament(name, location, start_date, end_date)
            else:
                self.display_error("Tipo de torneio inválido!")
                self.pause()
                return

            self.controller.create_tournament(tournament)
            self.display_success(f"Torneio '{name}' criado com sucesso!")
        except ValueError as e:
            self.display_error(str(e))
        except Exception as e:
            self.display_error(f"Erro ao criar torneio: {str(e)}")

        self.pause()

    def list_tournaments_screen(self):
        """Screen for listing all tournaments."""
        self.clear_screen()
        self.display_separator()
        print("           LISTA DE TORNEIOS")
        self.display_separator()

        try:
            tournaments = self.controller.get_all_tournaments()
            
            if not tournaments:
                print("\nNenhum torneio registrado ainda.")
            else:
                print(f"\nTotal de torneios: {len(tournaments)}\n")
                for i, tournament in enumerate(tournaments, 1):
                    print(f"{i}. {tournament.name}")
                    print(f"   Local: {tournament.location}")
                    print(f"   Data: {tournament.start_date} a {tournament.end_date}")
                    
                    # Display type-specific information
                    if isinstance(tournament, SwissTournament):
                        print(f"   Tipo: Suíço ({tournament.rounds} rodadas)")
                    elif isinstance(tournament, EliminatoryTournament):
                        print(f"   Tipo: Eliminatório")
                    else:
                        print(f"   Tipo: Básico")
                    print()
        except Exception as e:
            self.display_error(f"Erro ao listar torneios: {str(e)}")

        self.pause()

    def manage_tournament_screen(self):
        """Screen for managing a specific tournament."""
        self.clear_screen()
        self.display_separator()
        print("           GERENCIAR TORNEIO")
        self.display_separator()

        try:
            # List available tournaments
            tournaments = self.controller.get_all_tournaments()
            
            if not tournaments:
                print("\nNenhum torneio disponível para gerenciar.")
                self.pause()
                return

            print("\nTorneios disponíveis:")
            for i, tournament in enumerate(tournaments, 1):
                print(f"{i}. {tournament.name}")

            choice = self.get_input("\nEscolha o número do torneio (0 para cancelar): ")
            
            if choice == '0':
                return

            try:
                index = int(choice) - 1
                if index < 0 or index >= len(tournaments):
                    self.display_error("Opção inválida!")
                    self.pause()
                    return

                selected_tournament = tournaments[index]
                self._manage_tournament_menu(selected_tournament)
            except ValueError:
                self.display_error("Entrada inválida!")
                self.pause()
        except Exception as e:
            self.display_error(f"Erro ao gerenciar torneio: {str(e)}")
            self.pause()

    def _manage_tournament_menu(self, tournament):
        """Display management menu for a specific tournament."""
        while True:
            self.clear_screen()
            self.display_separator()
            print(f"       GERENCIAR TORNEIO: {tournament.name}")
            self.display_separator()
            print("1 - Ver detalhes")
            print("2 - Adicionar jogador")
            print("3 - Remover jogador")
            print("4 - Ver ranking inicial")
            print("5 - Listar jogadores inscritos")
            print("6 - Editar torneio")
            print("7 - Excluir torneio")
            print("8 - Voltar")
            self.display_separator()

            choice = self.get_input("\nEscolha uma opção: ")

            if choice == '1':
                self._view_tournament_details(tournament)
            elif choice == '2':
                self._add_player_to_tournament(tournament)
                # Reload tournament to get updated data
                tournament = self.controller.get_tournament_by_name(tournament.name)
            elif choice == '3':
                self._remove_player_from_tournament(tournament)
                # Reload tournament to get updated data
                tournament = self.controller.get_tournament_by_name(tournament.name)
            elif choice == '4':
                self._view_tournament_ranking(tournament)
            elif choice == '5':
                self._list_tournament_players(tournament)
            elif choice == '6':
                self._edit_tournament(tournament)
                break
            elif choice == '7':
                if self._delete_tournament(tournament):
                    break
            elif choice == '8':
                break
            else:
                self.display_error("Opção inválida!")
                self.pause()

    def _view_tournament_details(self, tournament):
        """Display detailed information about a tournament."""
        self.clear_screen()
        self.display_separator()
        print("           DETALHES DO TORNEIO")
        self.display_separator()
        
        print(f"\nNome: {tournament.name}")
        print(f"Local: {tournament.location}")
        print(f"Data de início: {tournament.start_date}")
        print(f"Data de término: {tournament.end_date}")
        
        if isinstance(tournament, SwissTournament):
            print(f"Tipo: Torneio Suíço")
            print(f"Número de rodadas: {tournament.rounds}")
        elif isinstance(tournament, EliminatoryTournament):
            print(f"Tipo: Torneio Eliminatório")
        else:
            print(f"Tipo: Torneio Básico")
        
        self.pause()

    def _edit_tournament(self, tournament):
        """Edit tournament information."""
        self.clear_screen()
        self.display_separator()
        print("           EDITAR TORNEIO")
        self.display_separator()

        try:
            old_name = tournament.name
            
            print(f"\nDeixe em branco para manter o valor atual.")
            name = self.get_input(f"Nome [{tournament.name}]: ") or tournament.name
            location = self.get_input(f"Local [{tournament.location}]: ") or tournament.location
            start_date = self.get_input(f"Data de início [{tournament.start_date}]: ") or tournament.start_date
            end_date = self.get_input(f"Data de término [{tournament.end_date}]: ") or tournament.end_date

            # Update based on tournament type
            if isinstance(tournament, SwissTournament):
                rounds_input = self.get_input(f"Número de rodadas [{tournament.rounds}]: ")
                rounds = int(rounds_input) if rounds_input else tournament.rounds
                updated_tournament = SwissTournament(name, location, start_date, end_date, rounds)
            elif isinstance(tournament, EliminatoryTournament):
                updated_tournament = EliminatoryTournament(name, location, start_date, end_date)
            else:
                from src.entities.tournament import Tournament
                updated_tournament = Tournament(name, location, start_date, end_date)

            self.controller.update_tournament(old_name, updated_tournament)
            self.display_success(f"Torneio '{name}' atualizado com sucesso!")
        except ValueError as e:
            self.display_error(str(e))
        except Exception as e:
            self.display_error(f"Erro ao editar torneio: {str(e)}")

        self.pause()

    def _delete_tournament(self, tournament) -> bool:
        """Delete a tournament after confirmation."""
        self.clear_screen()
        self.display_separator()
        print("           EXCLUIR TORNEIO")
        self.display_separator()

        print(f"\n⚠️  Tem certeza que deseja excluir o torneio '{tournament.name}'?")
        confirm = self.get_input("Digite 'SIM' para confirmar: ")

        if confirm.upper() == 'SIM':
            try:
                self.controller.delete_tournament(tournament.name)
                self.display_success(f"Torneio '{tournament.name}' excluído com sucesso!")
                self.pause()
                return True
            except Exception as e:
                self.display_error(f"Erro ao excluir torneio: {str(e)}")
                self.pause()
                return False
        else:
            self.display_message("Operação cancelada.")
            self.pause()
            return False

    def _add_player_to_tournament(self, tournament):
        """Add a player to the tournament."""
        self.clear_screen()
        self.display_separator()
        print("           ADICIONAR JOGADOR AO TORNEIO")
        self.display_separator()

        try:
            # Get all available players
            all_players = self.player_controller.get_all_players()
            
            if not all_players:
                print("\nNenhum jogador cadastrado no sistema.")
                print("Por favor, cadastre jogadores primeiro.")
                self.pause()
                return

            # Show current players in tournament
            current_players = tournament.players
            if current_players:
                print(f"\nJogadores já inscritos ({len(current_players)}):")
                for p in current_players:
                    print(f"  - {p.name}")

            # Show available players (not in tournament)
            available_players = [p for p in all_players if p.name not in [cp.name for cp in current_players]]
            
            if not available_players:
                print("\nTodos os jogadores cadastrados já estão inscritos neste torneio.")
                self.pause()
                return

            print(f"\nJogadores disponíveis:")
            for i, player in enumerate(available_players, 1):
                print(f"{i}. {player.name} (Rating Clássico: {player.rating.classic})")

            choice = self.get_input("\nEscolha o número do jogador (0 para cancelar): ")
            
            if choice == '0':
                return

            try:
                index = int(choice) - 1
                if index < 0 or index >= len(available_players):
                    self.display_error("Opção inválida!")
                    self.pause()
                    return

                selected_player = available_players[index]
                self.controller.add_player_to_tournament(tournament.name, selected_player)
                self.display_success(f"Jogador '{selected_player.name}' adicionado ao torneio!")
            except ValueError:
                self.display_error("Entrada inválida!")
        except Exception as e:
            self.display_error(f"Erro ao adicionar jogador: {str(e)}")

        self.pause()

    def _remove_player_from_tournament(self, tournament):
        """Remove a player from the tournament."""
        self.clear_screen()
        self.display_separator()
        print("           REMOVER JOGADOR DO TORNEIO")
        self.display_separator()

        try:
            players = tournament.players
            
            if not players:
                print("\nNenhum jogador inscrito neste torneio.")
                self.pause()
                return

            print(f"\nJogadores inscritos:")
            for i, player in enumerate(players, 1):
                print(f"{i}. {player.name}")

            choice = self.get_input("\nEscolha o número do jogador para remover (0 para cancelar): ")
            
            if choice == '0':
                return

            try:
                index = int(choice) - 1
                if index < 0 or index >= len(players):
                    self.display_error("Opção inválida!")
                    self.pause()
                    return

                selected_player = players[index]
                
                # Confirm removal
                confirm = self.get_input(f"\n⚠️  Remover '{selected_player.name}' do torneio? (S/N): ")
                
                if confirm.upper() == 'S':
                    self.controller.remove_player_from_tournament(tournament.name, selected_player.name)
                    self.display_success(f"Jogador '{selected_player.name}' removido do torneio!")
                else:
                    self.display_message("Operação cancelada.")
            except ValueError:
                self.display_error("Entrada inválida!")
        except Exception as e:
            self.display_error(f"Erro ao remover jogador: {str(e)}")

        self.pause()

    def _view_tournament_ranking(self, tournament):
        """View the initial ranking of players in the tournament."""
        self.clear_screen()
        self.display_separator()
        print("           RANKING INICIAL DO TORNEIO")
        self.display_separator()

        try:
            players = tournament.players
            
            if not players:
                print("\nNenhum jogador inscrito neste torneio.")
                self.pause()
                return

            # Ask which rating type to use for ranking
            print("\nTipo de rating para o ranking:")
            print("1 - Clássico")
            print("2 - Rápido")
            print("3 - Blitz")
            
            rating_choice = self.get_input("\nEscolha o tipo: ")
            
            rating_map = {'1': 'classic', '2': 'rapid', '3': 'blitz'}
            rating_type = rating_map.get(rating_choice, 'classic')
            rating_name = {'classic': 'Clássico', 'rapid': 'Rápido', 'blitz': 'Blitz'}[rating_type]

            ranked_players = self.controller.get_tournament_ranking(tournament.name, rating_type)

            print(f"\n{'='*60}")
            print(f"RANKING INICIAL - Rating {rating_name}")
            print(f"{'='*60}")
            print(f"\nTotal de jogadores: {len(ranked_players)}\n")
            
            for i, player in enumerate(ranked_players, 1):
                rating_value = getattr(player.rating, rating_type)
                print(f"{i}º lugar - {player.name}")
                print(f"   Rating {rating_name}: {rating_value}")
                print(f"   Ratings: Clássico: {player.rating.classic} | Rápido: {player.rating.rapid} | Blitz: {player.rating.blitz}")
                print()
        except Exception as e:
            self.display_error(f"Erro ao visualizar ranking: {str(e)}")

        self.pause()

    def _list_tournament_players(self, tournament):
        """List all players registered in the tournament."""
        self.clear_screen()
        self.display_separator()
        print("           JOGADORES INSCRITOS NO TORNEIO")
        self.display_separator()

        try:
            players = tournament.players
            
            if not players:
                print("\nNenhum jogador inscrito neste torneio.")
            else:
                print(f"\nTotal de jogadores inscritos: {len(players)}\n")
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
