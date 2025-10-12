from .base_view import BaseView
from src.controllers.tournament_controller import TournamentController
from src.controllers.player_controller import PlayerController
from src.entities.swiss_tournament import SwissTournament
from src.entities.eliminatory_tournament import EliminatoryTournament
from src.entities.time_control import TimeControl


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

            # Select time control
            print("\nRitmo de jogo:")
            print("1 - Clássico")
            print("2 - Rápido")
            print("3 - Blitz")
            time_control_choice = self.get_input("\nEscolha o ritmo: ")

            time_control_map = {
                '1': TimeControl.CLASSIC,
                '2': TimeControl.RAPID,
                '3': TimeControl.BLITZ
            }

            time_control = time_control_map.get(time_control_choice)
            if time_control is None:
                self.display_error("Ritmo de jogo inválido!")
                self.pause()
                return

            # Select tournament type
            print("\nTipo de torneio:")
            print("1 - Torneio Suíço")
            print("2 - Torneio Eliminatório")
            tournament_type = self.get_input("\nEscolha o tipo: ")

            if tournament_type == '1':
                # Swiss tournament
                rounds = int(self.get_input("Número de rodadas: "))
                tournament = SwissTournament(name, location, start_date, end_date, time_control, rounds)
            elif tournament_type == '2':
                # Eliminatory tournament
                tournament = EliminatoryTournament(name, location, start_date, end_date, time_control)
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
                    print(f"   Ritmo: {tournament.time_control}")
                    
                    # Display type-specific information
                    if isinstance(tournament, SwissTournament):
                        print(f"   Tipo: Suíço ({tournament.num_rounds} rodadas)")
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

    def _can_generate_next_round(self, tournament) -> bool:
        """
        Check if the next round can be generated.
        Returns True if there are no rounds or if all results from the last round are annotated.
        
        Args:
            tournament: The tournament to check.
            
        Returns:
            bool: True if next round can be generated, False otherwise.
        """
        # If no rounds exist, can generate first round
        if not tournament.rounds or len(tournament.rounds) == 0:
            return True
        
        # Get the last round
        last_round = tournament.rounds[-1]
        
        # Check if all matches have results
        for match in last_round.matches:
            # BYE matches don't need results (white wins automatically)
            if match.black is None:
                continue
            
            # If any match doesn't have a result, can't generate next round
            if match.result is None:
                return False
        
        return True

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
            print("4 - Ver rankings")
            print("5 - Listar jogadores inscritos")
            
            # Check if next round can be generated
            can_generate = self._can_generate_next_round(tournament)
            
            if can_generate:
                print(f"6 - Gerar emparceiramento ({tournament.get_current_round_number()}ª rodada)")
            else:
                print(f"6 - Anotar resultados ({len(tournament.rounds)}ª rodada) - OBRIGATÓRIO")
            
            print("7 - Editar torneio")
            print("8 - Excluir torneio")
            print("9 - Voltar")
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
                self._view_rankings_menu(tournament)
            elif choice == '5':
                self._list_tournament_players(tournament)
            elif choice == '6':
                if can_generate:
                    self._generate_round_pairings(tournament)
                else:
                    self._annotate_results(tournament)
                # Reload tournament to get updated data
                tournament = self.controller.get_tournament_by_name(tournament.name)
            elif choice == '7':
                self._edit_tournament(tournament)
                break
            elif choice == '8':
                if self._delete_tournament(tournament):
                    break
            elif choice == '9':
                break
            else:
                self.display_error("Opção inválida!")
                self.pause()
                # Reload tournament to get updated data
                tournament = self.controller.get_tournament_by_name(tournament.name)

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
        print(f"Ritmo de jogo: {tournament.time_control}")
        
        if isinstance(tournament, SwissTournament):
            print(f"Tipo: Torneio Suíço")
            print(f"Número de rodadas: {tournament.num_rounds}")
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

            # Time control selection
            print(f"\nRitmo de jogo atual: {tournament.time_control}")
            print("Deixe em branco para manter, ou escolha:")
            print("1 - Clássico")
            print("2 - Rápido")
            print("3 - Blitz")
            time_control_input = self.get_input("Nova escolha: ")
            
            time_control_map = {
                '1': TimeControl.CLASSIC,
                '2': TimeControl.RAPID,
                '3': TimeControl.BLITZ
            }
            time_control = time_control_map.get(time_control_input, tournament.time_control)

            # Update based on tournament type
            if isinstance(tournament, SwissTournament):
                rounds_input = self.get_input(f"Número de rodadas [{tournament.num_rounds}]: ")
                rounds = int(rounds_input) if rounds_input else tournament.num_rounds
                updated_tournament = SwissTournament(name, location, start_date, end_date, time_control, rounds)
            elif isinstance(tournament, EliminatoryTournament):
                updated_tournament = EliminatoryTournament(name, location, start_date, end_date, time_control)
            else:
                from src.entities.tournament import Tournament
                updated_tournament = Tournament(name, location, start_date, end_date, time_control)

            # Copy players from old tournament to updated tournament
            for player in tournament.players:
                updated_tournament.add_player(player)

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

    def _view_rankings_menu(self, tournament):
        """Display the rankings menu with options for initial and round rankings."""
        while True:
            self.clear_screen()
            self.display_separator()
            print(f"       RANKINGS - {tournament.name}")
            self.display_separator()
            print("1 - Ranking Inicial")
            
            # Show ranking options for each completed round
            if tournament.rounds:
                for i, round_obj in enumerate(tournament.rounds, 1):
                    # Check if round has all results
                    all_results = all(
                        match.result is not None or match.black is None 
                        for match in round_obj.matches
                    )
                    status = "✓" if all_results else "⚠"
                    print(f"{i + 1} - Ranking após {i}ª rodada {status}")
            
            print("0 - Voltar")
            self.display_separator()

            choice = self.get_input("\nEscolha uma opção: ")

            if choice == '0':
                break
            elif choice == '1':
                self._view_tournament_ranking(tournament, is_initial=True)
            else:
                # Check if it's a round ranking
                try:
                    round_index = int(choice) - 2  # Subtract 2 (option 1 is initial, option 2 is round 1)
                    if 0 <= round_index < len(tournament.rounds):
                        self._view_round_ranking(tournament, round_index + 1)
                    else:
                        self.display_error("Opção inválida!")
                        self.pause()
                except ValueError:
                    self.display_error("Opção inválida!")
                    self.pause()

    def _view_tournament_ranking(self, tournament, is_initial=True):
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

            # Use the tournament's time control for ranking
            rating_type = tournament.time_control.value
            rating_name = str(tournament.time_control)

            print(f"\nRitmo do torneio: {rating_name}")
            print(f"O ranking será baseado no rating {rating_name}\n")

            # Allow user to choose a different rating if desired
            use_tournament_rating = self.get_input("Deseja usar um rating diferente? (S/N): ")
            
            if use_tournament_rating.upper() == 'S':
                print("\nTipo de rating para o ranking:")
                print("1 - Clássico")
                print("2 - Rápido")
                print("3 - Blitz")
                
                rating_choice = self.get_input("\nEscolha o tipo: ")
                
                rating_map = {'1': 'classic', '2': 'rapid', '3': 'blitz'}
                rating_type = rating_map.get(rating_choice, rating_type)
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

    def _view_round_ranking(self, tournament, round_number):
        """View the ranking after a specific round."""
        self.clear_screen()
        self.display_separator()
        print(f"           RANKING APÓS {round_number}ª RODADA")
        self.display_separator()

        try:
            players = tournament.players
            
            if not players:
                print("\nNenhum jogador inscrito neste torneio.")
                self.pause()
                return
            
            # Check if the round exists
            if round_number > len(tournament.rounds):
                self.display_error(f"A {round_number}ª rodada ainda não foi gerada!")
                self.pause()
                return

            # Calculate scores up to this round
            player_scores = {}
            
            for player in players:
                player_scores[player.name] = {
                    'player': player,
                    'score': 0.0,
                    'matches_played': 0
                }
            
            # Calculate scores from all rounds up to round_number
            for i in range(round_number):
                if i >= len(tournament.rounds):
                    break
                    
                round_obj = tournament.rounds[i]
                
                for match in round_obj.matches:
                    white_name = match.white.name
                    
                    if match.black is None:
                        # BYE - automatic win
                        player_scores[white_name]['score'] += 1.0
                        player_scores[white_name]['matches_played'] += 1
                    elif match.result:
                        player_scores[white_name]['matches_played'] += 1
                        
                        black_name = match.black.name
                        player_scores[black_name]['matches_played'] += 1
                        
                        if match.result == "1-0":
                            player_scores[white_name]['score'] += 1.0
                        elif match.result == "0-1":
                            player_scores[black_name]['score'] += 1.0
                        elif match.result == "0.5-0.5":
                            player_scores[white_name]['score'] += 0.5
                            player_scores[black_name]['score'] += 0.5

            # Sort players by score (descending), then by rating (descending)
            rating_type = tournament.time_control.value
            rating_name = str(tournament.time_control)
            
            sorted_players = sorted(
                player_scores.values(),
                key=lambda x: (
                    -x['score'],
                    -getattr(x['player'].rating, rating_type)
                )
            )

            print(f"\nRitmo do torneio: {rating_name}")
            print(f"Rodadas contabilizadas: 1 até {round_number}")
            print(f"\n{'='*80}")
            print(f"RANKING APÓS {round_number}ª RODADA")
            print(f"{'='*80}")
            print(f"\nTotal de jogadores: {len(sorted_players)}\n")
            
            for i, data in enumerate(sorted_players, 1):
                player = data['player']
                score = data['score']
                matches = data['matches_played']
                rating_value = getattr(player.rating, rating_type)
                
                print(f"{i}º lugar - {player.name}")
                print(f"   Pontuação: {score:.1f} pontos ({matches} partidas)")
                print(f"   Rating {rating_name}: {rating_value}")
                print()
                
        except Exception as e:
            self.display_error(f"Erro ao visualizar ranking: {str(e)}")
            import traceback
            traceback.print_exc()

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

    def _generate_round_pairings(self, tournament):
        """Generate and display pairings for the next round."""
        self.clear_screen()
        self.display_separator()
        print("           GERAR EMPARCEIRAMENTO")
        self.display_separator()

        try:
            # Check if tournament has players
            if len(tournament.players) < 2:
                self.display_error("O torneio precisa de pelo menos 2 jogadores para gerar emparceiramentos.")
                self.pause()
                return

            # Show tournament info
            print(f"\nTorneio: {tournament.name}")
            print(f"Tipo: {'Suíço' if isinstance(tournament, SwissTournament) else 'Eliminatório'}")
            print(f"Ritmo: {tournament.time_control}")
            print(f"Jogadores inscritos: {len(tournament.players)}")

            # Get bracket info for eliminatory tournaments
            if isinstance(tournament, EliminatoryTournament):
                bracket_info = self.controller.get_bracket_info(tournament.name)
                print(f"\nEstrutura do bracket:")
                print(f"  - Total de rodadas: {bracket_info['total_rounds']}")
                print(f"  - Tamanho do bracket: {bracket_info['bracket_size']}")
                if bracket_info['byes_in_first_round'] > 0:
                    print(f"  - Byes na primeira rodada: {bracket_info['byes_in_first_round']}")
                print(f"\nRodadas:")
                for round_num, round_name in bracket_info['round_names'].items():
                    print(f"  Rodada {round_num}: {round_name}")

            # Generate pairings
            print("\n" + "="*60)
            confirm = self.get_input("\nGerar emparceiramento da próxima rodada? (S/N): ")

            if confirm.upper() != 'S':
                self.display_message("Operação cancelada.")
                self.pause()
                return

            round_number, pairings, tournament_obj = self.controller.generate_round_pairings(tournament.name)

            # Display pairings
            self.clear_screen()
            self.display_separator()
            
            if isinstance(tournament, EliminatoryTournament):
                bracket_info = self.controller.get_bracket_info(tournament.name)
                round_name = bracket_info['round_names'].get(round_number, f"Rodada {round_number}")
                print(f"    EMPARCEIRAMENTO - {round_name.upper()}")
            else:
                print(f"           EMPARCEIRAMENTO - RODADA {round_number}")
            
            self.display_separator()

            print(f"\nTorneio: {tournament.name}")
            print(f"Rodada: {round_number}")
            print(f"Total de partidas: {len(pairings)}\n")

            for i, (white, black) in enumerate(pairings, 1):
                print(f"Mesa {i}:")
                print(f"  Brancas: {white.name}")
                if black is None:
                    print(f"  Pretas: BYE (vitória automática)")
                else:
                    print(f"  Pretas: {black.name}")
                print()

            # Confirm save
            print("="*60)
            save_confirm = self.get_input("\nSalvar este emparceiramento? (S/N): ")

            if save_confirm.upper() == 'S':
                self.controller.save_round_pairings(tournament.name, round_number, pairings)
                self.display_success(f"Emparceiramento da rodada {round_number} salvo com sucesso!")
            else:
                self.display_message("Emparceiramento não foi salvo.")

        except ValueError as e:
            self.display_error(str(e))
        except Exception as e:
            self.display_error(f"Erro ao gerar emparceiramento: {str(e)}")

        self.pause()

    def _annotate_results(self, tournament):
        """Annotate results for matches in a specific round."""
        try:
            self.clear_screen()
            self.display_separator()
            print(f"       ANOTAR RESULTADOS: {tournament.name}")
            self.display_separator()

            # Check if there are any rounds
            if not tournament.rounds or len(tournament.rounds) == 0:
                self.display_error("Não há rodadas geradas neste torneio!")
                self.pause()
                return

            # Let user select which round to annotate
            print("\nRodadas disponíveis:")
            for i, round_obj in enumerate(tournament.rounds, 1):
                print(f"{i} - Rodada {round_obj.round_}")
            
            round_choice = self.get_input("\nQual rodada deseja anotar? (ou 0 para voltar): ")

            if round_choice == '0':
                return

            try:
                round_index = int(round_choice) - 1
                if round_index < 0 or round_index >= len(tournament.rounds):
                    self.display_error("Rodada inválida!")
                    self.pause()
                    return
            except ValueError:
                self.display_error("Entrada inválida!")
                self.pause()
                return

            round_number = tournament.rounds[round_index].round_

            # Get matches for this round
            matches = self.controller.get_round_matches(tournament.name, round_number)

            if not matches or len(matches) == 0:
                self.display_error("Esta rodada não possui partidas!")
                self.pause()
                return

            # Cursor-based result annotation
            cursor_pos = 0

            while True:
                self.clear_screen()
                self.display_separator()
                print(f"       ANOTAR RESULTADOS - Rodada {round_number}")
                self.display_separator()
                print("\nComandos:")
                print("  B - Brancas vencem (1-0)")
                print("  P - Pretas vencem (0-1)")
                print("  E - Empate (½-½)")
                print("  Enter - Próxima partida")
                print("  Q - Sair e salvar")
                self.display_separator()

                # Display all matches with cursor
                for i, match in enumerate(matches):
                    cursor = ">>>" if i == cursor_pos else "   "
                    
                    # Display result
                    result_display = ""
                    if match.result == "1-0":
                        result_display = " [1-0]"
                    elif match.result == "0-1":
                        result_display = " [0-1]"
                    elif match.result == "0.5-0.5":
                        result_display = " [½-½]"
                    else:
                        result_display = " [ - ]"

                    print(f"\n{cursor} Mesa {i+1}:{result_display}")
                    print(f"    Brancas: {match.white.name}")
                    if match.black is None:
                        print(f"    Pretas: BYE (vitória automática)")
                    else:
                        print(f"    Pretas: {match.black.name}")

                # Get user input
                print("\n" + "="*60)
                command = self.get_input("\nComando: ").upper()

                if command == 'B':
                    # White wins
                    if matches[cursor_pos].black is None:
                        self.display_error("Esta partida já é BYE (vitória automática)!")
                        self.pause()
                    else:
                        self.controller.update_match_result(
                            tournament.name, 
                            round_number, 
                            cursor_pos, 
                            "1-0"
                        )
                        # Reload matches
                        matches = self.controller.get_round_matches(tournament.name, round_number)
                        cursor_pos = min(cursor_pos + 1, len(matches) - 1)

                elif command == 'P':
                    # Black wins
                    if matches[cursor_pos].black is None:
                        self.display_error("Esta partida é BYE - brancas vencem automaticamente!")
                        self.pause()
                    else:
                        self.controller.update_match_result(
                            tournament.name, 
                            round_number, 
                            cursor_pos, 
                            "0-1"
                        )
                        # Reload matches
                        matches = self.controller.get_round_matches(tournament.name, round_number)
                        cursor_pos = min(cursor_pos + 1, len(matches) - 1)

                elif command == 'E':
                    # Draw
                    if matches[cursor_pos].black is None:
                        self.display_error("Esta partida é BYE - não pode haver empate!")
                        self.pause()
                    else:
                        self.controller.update_match_result(
                            tournament.name, 
                            round_number, 
                            cursor_pos, 
                            "0.5-0.5"
                        )
                        # Reload matches
                        matches = self.controller.get_round_matches(tournament.name, round_number)
                        cursor_pos = min(cursor_pos + 1, len(matches) - 1)

                elif command == '' or command == '\n':
                    # Move to next match
                    cursor_pos = (cursor_pos + 1) % len(matches)

                elif command == 'Q':
                    # Quit and save
                    self.display_success("Resultados salvos com sucesso!")
                    self.pause()
                    break

                else:
                    self.display_error("Comando inválido!")
                    self.pause()

        except ValueError as e:
            self.display_error(str(e))
            self.pause()
        except Exception as e:
            self.display_error(f"Erro ao anotar resultados: {str(e)}")
            self.pause()
