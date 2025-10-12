from .base_view import BaseView
from src.controllers.tournament_controller import TournamentController
from src.controllers.player_controller import PlayerController
from src.entities.swiss_tournament import SwissTournament
from src.entities.eliminatory_tournament import EliminatoryTournament
from src.entities.time_control import TimeControl
import traceback

class TournamentView(BaseView):
    """View class for managing tournament-related screens."""

    def __init__(self):
        self.controller = TournamentController()
        self.player_controller = PlayerController()

    def show_menu(self):
        """Display the tournament menu and handle user input."""
        menu_options = {
            '1': self.create_tournament_screen,
            '2': self.list_tournaments_screen,
            '3': self.manage_tournament_screen,
            '4': None  # Sair
        }

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
            action = menu_options.get(choice)

            if action:
                action()
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
            name, location, start_date, end_date = self._get_tournament_basic_info()
            time_control = self._get_time_control_choice()
            if time_control is None:
                return

            tournament = self._get_tournament_type_and_rounds(name, location, start_date, end_date, time_control)
            if tournament is None:
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
                    self._display_tournament_info(i, tournament)
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
            selected_tournament = self._get_tournament_choice()
            if selected_tournament:
                self._manage_tournament_menu(selected_tournament)
        except Exception as e:
            self.display_error(f"Erro ao gerenciar torneio: {str(e)}")
            self.pause()

    def _get_tournament_basic_info(self):
        name = self.get_input("\nNome do torneio: ")
        location = self.get_input("Local: ")
        start_date = self.get_input("Data de início (YYYY-MM-DD): ")
        end_date = self.get_input("Data de término (YYYY-MM-DD): ")
        return name, location, start_date, end_date

    def _get_time_control_choice(self):
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
        return time_control

    def _get_tournament_type_and_rounds(self, name, location, start_date, end_date, time_control):
        print("\nTipo de torneio:")
        print("1 - Torneio Suíço")
        print("2 - Torneio Eliminatório")
        tournament_type = self.get_input("\nEscolha o tipo: ")

        if tournament_type == '1':
            rounds = int(self.get_input("Número de rodadas: "))
            return SwissTournament(name, location, start_date, end_date, time_control, rounds)
        elif tournament_type == '2':
            return EliminatoryTournament(name, location, start_date, end_date, time_control)
        else:
            self.display_error("Tipo de torneio inválido!")
            self.pause()
            return None

    def _display_tournament_info(self, index, tournament):
        print(f"{index}. {tournament.name}")
        print(f"   Local: {tournament.location}")
        print(f"   Data: {tournament.start_date} a {tournament.end_date}")
        print(f"   Ritmo: {tournament.time_control}")

        if isinstance(tournament, SwissTournament):
            print(f"   Tipo: Suíço ({tournament.num_rounds} rodadas)")
        elif isinstance(tournament, EliminatoryTournament):
            print(f"   Tipo: Eliminatório")
        else:
            print(f"   Tipo: Básico")
        print()

    def _get_tournament_choice(self):
        tournaments = self.controller.get_all_tournaments()

        if not tournaments:
            print("\nNenhum torneio disponível para gerenciar.")
            self.pause()
            return None

        print("\nTorneios disponíveis:")
        for i, tournament in enumerate(tournaments, 1):
            print(f"{i}. {tournament.name}")

        choice = self.get_input("\nEscolha o número do torneio (0 para cancelar): ")

        if choice == '0':
            return None

        try:
            index = int(choice) - 1
            if 0 <= index < len(tournaments):
                return tournaments[index]
            else:
                self.display_error("Opção inválida!")
                self.pause()
                return None
        except ValueError:
            self.display_error("Entrada inválida!")
            self.pause()
            return None

    def _manage_tournament_menu(self, tournament):
        """Display management menu for a specific tournament."""
        menu_actions = {
            '1': self._view_tournament_details,
            '2': self._add_player_to_tournament,
            '3': self._remove_player_from_tournament,
            '4': self._view_rankings_menu,
            '5': self._list_tournament_players,
            '7': self._edit_tournament,
            '8': self._delete_tournament
        }
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

            if choice == '9':
                break

            action = menu_actions.get(choice)
            if action:
                action(tournament)
                if choice in ['2', '3', '6', '7', '8']:
                    tournament = self.controller.get_tournament_by_name(tournament.name)
            elif choice == '6':
                if can_generate:
                    self._generate_round_pairings(tournament)
                else:
                    self._annotate_results(tournament)
                tournament = self.controller.get_tournament_by_name(tournament.name)
            else:
                self.display_error("Opção inválida!")
                self.pause()

    def _can_generate_next_round(self, tournament) -> bool:
        if not tournament.rounds:
            return True

        last_round = tournament.rounds[-1]
        return all(match.result is not None or match.black is None for match in last_round.matches)

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

            time_control = self._get_time_control_choice() or tournament.time_control

            if isinstance(tournament, SwissTournament):
                rounds_input = self.get_input(f"Número de rodadas [{tournament.num_rounds}]: ")
                rounds = int(rounds_input) if rounds_input else tournament.num_rounds
                updated_tournament = SwissTournament(name, location, start_date, end_date, time_control, rounds)
            elif isinstance(tournament, EliminatoryTournament):
                updated_tournament = EliminatoryTournament(name, location, start_date, end_date, time_control)
            else:
                from src.entities.tournament import Tournament
                updated_tournament = Tournament(name, location, start_date, end_date, time_control)

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
            all_players = self.player_controller.get_all_players()
            
            if not all_players:
                print("\nNenhum jogador cadastrado no sistema.")
                print("Por favor, cadastre jogadores primeiro.")
                self.pause()
                return

            current_players = tournament.players
            if current_players:
                print(f"\nJogadores já inscritos ({len(current_players)}):")
                for p in current_players:
                    print(f"  - {p.name}")

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
                if 0 <= index < len(available_players):
                    selected_player = available_players[index]
                    self.controller.add_player_to_tournament(tournament.name, selected_player)
                    self.display_success(f"Jogador '{selected_player.name}' adicionado ao torneio!")
                else:
                    self.display_error("Opção inválida!")
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
                if 0 <= index < len(players):
                    selected_player = players[index]
                    confirm = self.get_input(f"\n⚠️  Remover '{selected_player.name}' do torneio? (S/N): ")
                    
                    if confirm.upper() == 'S':
                        self.controller.remove_player_from_tournament(tournament.name, selected_player.name)
                        self.display_success(f"Jogador '{selected_player.name}' removido do torneio!")
                    else:
                        self.display_message("Operação cancelada.")
                else:
                    self.display_error("Opção inválida!")
            except ValueError:
                self.display_error("Entrada inválida!")
        except Exception as e:
            self.display_error(f"Erro ao remover jogador: {str(e)}")

        self.pause()

    def _view_rankings_menu(self, tournament):
        """Display the rankings menu."""
        while True:
            self.clear_screen()
            self.display_separator()
            print(f"       RANKINGS - {tournament.name}")
            self.display_separator()
            print("1 - Ranking Inicial")

            for i, round_obj in enumerate(tournament.rounds or [], 1):
                all_results = all(m.result is not None or m.black is None for m in round_obj.matches)
                status = "✓" if all_results else "⚠"
                print(f"{i + 1} - Ranking após {i}ª rodada {status}")

            print("0 - Voltar")
            self.display_separator()

            choice = self.get_input("\nEscolha uma opção: ")

            if choice == '0':
                break
            elif choice == '1':
                self._view_tournament_ranking(tournament)
            else:
                try:
                    round_index = int(choice) - 2
                    if 0 <= round_index < len(tournament.rounds):
                        self._view_round_ranking(tournament, round_index + 1)
                    else:
                        self.display_error("Opção inválida!")
                        self.pause()
                except ValueError:
                    self.display_error("Opção inválida!")
                    self.pause()

    def _view_tournament_ranking(self, tournament):
        """View the initial ranking of players in the tournament."""
        self.clear_screen()
        self.display_separator()
        print("           RANKING INICIAL DO TORNEIO")
        self.display_separator()

        try:
            if not tournament.players:
                print("\nNenhum jogador inscrito neste torneio.")
                self.pause()
                return

            rating_type, rating_name = self._get_ranking_type(tournament)
            if rating_type is None:
                return

            ranked_players = self.controller.get_tournament_ranking(tournament.name, rating_type)
            self._display_rankings(ranked_players, rating_name, rating_type)

        except Exception as e:
            self.display_error(f"Erro ao visualizar ranking: {str(e)}")

        self.pause()

    def _get_ranking_type(self, tournament):
        rating_type = tournament.time_control.value
        rating_name = str(tournament.time_control)
        print(f"\nRitmo do torneio: {rating_name}")
        print(f"O ranking será baseado no rating {rating_name}\n")
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

        return rating_type, rating_name

    def _display_rankings(self, ranked_players, rating_name, rating_type):
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

    def _view_round_ranking(self, tournament, round_number):
        """View the ranking after a specific round."""
        self.clear_screen()
        self.display_separator()
        print(f"           RANKING APÓS {round_number}ª RODADA")
        self.display_separator()

        try:
            if not tournament.players:
                print("\nNenhum jogador inscrito neste torneio.")
                self.pause()
                return
            
            if round_number > len(tournament.rounds):
                self.display_error(f"A {round_number}ª rodada ainda não foi gerada!")
                self.pause()
                return

            player_scores = self._calculate_player_scores(tournament, round_number)
            rating_type = tournament.time_control.value
            rating_name = str(tournament.time_control)
            
            sorted_players = sorted(
                player_scores.values(),
                key=lambda x: (-x['score'], -getattr(x['player'].rating, rating_type))
            )

            self._display_round_rankings_with_stats(tournament, sorted_players, rating_name, round_number, rating_type)
                
        except Exception as e:
            self.display_error(f"Erro ao visualizar ranking: {str(e)}")
            traceback.print_exc()

        self.pause()

    def _calculate_player_scores(self, tournament, round_number):
        player_scores = {
            p.name: {'player': p, 'score': 0.0, 'matches_played': 0}
            for p in tournament.players
        }
        for i in range(round_number):
            if i >= len(tournament.rounds):
                break
            round_obj = tournament.rounds[i]
            for match in round_obj.matches:
                self._update_scores_from_match(player_scores, match)
        return player_scores

    def _update_scores_from_match(self, player_scores, match):
        white_name = match.white.name
        if match.black is None:
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

    def _display_round_rankings(self, sorted_players, rating_name, round_number, rating_type):
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
            
            # Try to get performance statistics
            try:
                # Get tournament name from context (we'll need to pass it)
                # For now, we'll calculate a simple performance indicator
                if matches > 0:
                    percentage = (score / matches) * 100
                    print(f"   Performance: {percentage:.1f}%")
            except Exception:
                pass
            
            print()

    def _display_round_rankings_with_stats(self, tournament, sorted_players, rating_name, round_number, rating_type):
        """Display round rankings with full statistics including performance rating."""
        print(f"\nRitmo do torneio: {rating_name}")
        print(f"Rodadas contabilizadas: 1 até {round_number}")
        print(f"\n{'='*90}")
        print(f"RANKING APÓS {round_number}ª RODADA (com estatísticas)")
        print(f"{'='*90}")
        print(f"\nTotal de jogadores: {len(sorted_players)}\n")

        for i, data in enumerate(sorted_players, 1):
            player = data['player']
            score = data['score']
            matches = data['matches_played']
            rating_value = getattr(player.rating, rating_type)
            
            print(f"{i}º lugar - {player.name}")
            print(f"   Pontuação: {score:.1f} pontos ({matches} partidas)")
            print(f"   Rating {rating_name}: {rating_value}")
            
            # Get full statistics
            try:
                stats = self.controller.get_player_statistics(tournament.name, player.name)
                
                if stats['games_played'] > 0:
                    percentage = (stats['points'] / stats['games_played']) * 100
                    print(f"   Performance: {percentage:.1f}%")
                    print(f"   V/E/D: {stats['wins']}/{stats['draws']}/{stats['losses']}")
                
                if stats['average_opponent_rating'] > 0:
                    print(f"   Rating Médio dos Adversários: {stats['average_opponent_rating']:.0f}")
                    print(f"   Rating Performance: {stats['performance_rating']}")
                    print(f"   Ganho Estimado de Rating: {stats['rating_change']:.0f}")
            except Exception as e:
                # If stats fail, just show basic info
                if matches > 0:
                    percentage = (score / matches) * 100
                    print(f"   Performance: {percentage:.1f}%")
            
            print()

    def _list_tournament_players(self, tournament):
        """List all players registered in the tournament with their statistics."""
        self.clear_screen()
        self.display_separator()
        print("           JOGADORES INSCRITOS NO TORNEIO")
        self.display_separator()

        try:
            players = tournament.players
            
            if not players:
                print("\nNenhum jogador inscrito neste torneio.")
            else:
                # Check if there are any rounds (to show statistics)
                has_rounds = tournament.rounds and len(tournament.rounds) > 0
                
                print(f"\nTotal de jogadores inscritos: {len(players)}")
                
                if has_rounds:
                    print("\n(Incluindo estatísticas do torneio)")
                
                print()
                
                # Get rating type for this tournament
                rating_type = tournament.time_control.value
                
                for i, player in enumerate(players, 1):
                    current_rating = getattr(player.rating, rating_type)
                    
                    print(f"{i}. {player.name}")
                    print(f"   Data de Nascimento: {player.birthdate}")
                    print(f"   Gênero: {player.gender}")
                    print(f"   Ratings:")
                    print(f"     - Clássico: {player.rating.classic}")
                    print(f"     - Rápido: {player.rating.rapid}")
                    print(f"     - Blitz: {player.rating.blitz}")
                    
                    # Show tournament statistics if there are rounds
                    if has_rounds:
                        try:
                            stats = self.controller.get_player_statistics(tournament.name, player.name)
                            
                            print(f"   Desempenho no Torneio:")
                            print(f"     - Pontos: {stats['points']:.1f}/{stats['games_played']}")
                            print(f"     - Vitórias/Empates/Derrotas: {stats['wins']}/{stats['draws']}/{stats['losses']}")
                            
                            if stats['average_opponent_rating'] > 0:
                                print(f"     - Rating Médio dos Adversários: {stats['average_opponent_rating']:.0f}")
                                print(f"     - Rating Performance: {stats['performance_rating']}")
                                
                                # Calculate rating change (simplified)
                                rating_change = stats['performance_rating'] - current_rating
                                change_symbol = "+" if rating_change > 0 else ""
                                print(f"     - Ganho Estimado de Rating: {change_symbol}{rating_change:.0f}")
                        except Exception as e:
                            print(f"     - Estatísticas não disponíveis: {str(e)}")
                    
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
            if len(tournament.players) < 2:
                self.display_error("O torneio precisa de pelo menos 2 jogadores para gerar emparceiramentos.")
                self.pause()
                return

            self._display_tournament_summary(tournament)

            if isinstance(tournament, EliminatoryTournament):
                self._display_bracket_info(tournament)

            confirm = self.get_input("\nGerar emparceiramento da próxima rodada? (S/N): ")
            if confirm.upper() != 'S':
                self.display_message("Operação cancelada.")
                self.pause()
                return

            round_number, pairings, _ = self.controller.generate_round_pairings(tournament.name)
            self._display_and_save_pairings(tournament, round_number, pairings)

        except ValueError as e:
            self.display_error(str(e))
        except Exception as e:
            self.display_error(f"Erro ao gerar emparceiramento: {str(e)}")

        self.pause()

    def _display_tournament_summary(self, tournament):
        print(f"\nTorneio: {tournament.name}")
        print(f"Tipo: {'Suíço' if isinstance(tournament, SwissTournament) else 'Eliminatório'}")
        print(f"Ritmo: {tournament.time_control}")
        print(f"Jogadores inscritos: {len(tournament.players)}")

    def _display_bracket_info(self, tournament):
        bracket_info = self.controller.get_bracket_info(tournament.name)
        print(f"\nEstrutura do bracket:")
        print(f"  - Total de rodadas: {bracket_info['total_rounds']}")
        print(f"  - Tamanho do bracket: {bracket_info['bracket_size']}")
        if bracket_info['byes_in_first_round'] > 0:
            print(f"  - Byes na primeira rodada: {bracket_info['byes_in_first_round']}")
        print(f"\nRodadas:")
        for round_num, round_name in bracket_info['round_names'].items():
            print(f"  Rodada {round_num}: {round_name}")

    def _display_and_save_pairings(self, tournament, round_number, pairings):
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

        print("="*60)
        save_confirm = self.get_input("\nSalvar este emparceiramento? (S/N): ")
        if save_confirm.upper() == 'S':
            self.controller.save_round_pairings(tournament.name, round_number, pairings)
            self.display_success(f"Emparceiramento da rodada {round_number} salvo com sucesso!")
        else:
            self.display_message("Emparceiramento não foi salvo.")

    def _annotate_results(self, tournament):
        """Annotate results for matches in a specific round."""
        try:
            self.clear_screen()
            self.display_separator()
            print(f"       ANOTAR RESULTADOS: {tournament.name}")
            self.display_separator()

            if not tournament.rounds:
                self.display_error("Não há rodadas geradas neste torneio!")
                self.pause()
                return

            round_number = self._get_round_to_annotate(tournament)
            if round_number is None:
                return

            matches = self.controller.get_round_matches(tournament.name, round_number)
            if not matches:
                self.display_error("Esta rodada não possui partidas!")
                self.pause()
                return

            # Use different annotation method for eliminatory tournaments
            if isinstance(tournament, EliminatoryTournament):
                self._annotate_eliminatory_matches(tournament, round_number, matches)
            else:
                self._annotate_matches_cursor_based(tournament, round_number, matches)

        except ValueError as e:
            self.display_error(str(e))
            self.pause()
        except Exception as e:
            self.display_error(f"Erro ao anotar resultados: {str(e)}")
            self.pause()

    def _annotate_eliminatory_matches(self, tournament, round_number, matches):
        """
        Annotate results for eliminatory tournament matches using match scores.
        Format: Player1 X.X - Y.Y Player2 (e.g., Kasparov 2.5 - 1.5 Karpov)
        """
        self.clear_screen()
        self.display_separator()
        
        # Get round name
        bracket_info = self.controller.get_bracket_info(tournament.name)
        round_name = bracket_info['round_names'].get(round_number, f"Rodada {round_number}")
        
        print(f"       ANOTAR RESULTADOS - {round_name.upper()}")
        self.display_separator()
        print("\nDigite o placar de cada match no formato: X.X - Y.Y")
        print("Exemplo: 2.5 - 1.5 (significa que o jogador de brancas venceu 2.5 a 1.5)")
        print("\nPartidas:\n")

        for i, match in enumerate(matches, 1):
            print(f"Mesa {i}: {match.white.name} vs {match.black.name if match.black else 'BYE'}")
            
            if match.black is None:
                print(f"  → BYE (vitória automática para {match.white.name})")
                # Set result as 1-0 for BYE
                if match.result is None:
                    self.controller.update_match_result(tournament.name, round_number, i-1, "1-0")
            else:
                current_result = self._format_eliminatory_result(match.result)
                if current_result:
                    print(f"  → Resultado atual: {current_result}")
                else:
                    print(f"  → Sem resultado")

        print("\n" + "="*60)
        
        # Annotate each match
        for i, match in enumerate(matches, 1):
            if match.black is None:
                continue  # Skip BYE matches
            
            print(f"\nMesa {i}: {match.white.name} vs {match.black.name}")
            
            while True:
                score_input = self.get_input(f"Placar (ou 'pular' para manter resultado atual): ").strip()
                
                if score_input.lower() == 'pular':
                    break
                
                # Parse score input (e.g., "2.5 - 1.5" or "2.5-1.5")
                try:
                    parts = score_input.replace(" ", "").split("-")
                    if len(parts) != 2:
                        self.display_error("Formato inválido! Use: X.X - Y.Y")
                        continue
                    
                    white_score = float(parts[0])
                    black_score = float(parts[1])
                    
                    # Validate scores
                    if white_score < 0 or black_score < 0:
                        self.display_error("Pontuações devem ser positivas!")
                        continue
                    
                    # Determine winner and set result
                    if white_score > black_score:
                        result = "1-0"
                        winner = match.white.name
                    elif black_score > white_score:
                        result = "0-1"
                        winner = match.black.name
                    else:
                        self.display_error("Não pode haver empate em torneios eliminatórios!")
                        continue
                    
                    # Update match result
                    self.controller.update_match_result(tournament.name, round_number, i-1, result)
                    self.display_success(f"✓ {winner} avança (placar: {white_score} - {black_score})")
                    break
                    
                except ValueError:
                    self.display_error("Formato inválido! Use números decimais (ex: 2.5 - 1.5)")
                    continue
        
        print("\n" + "="*60)
        self.display_success("Resultados da rodada anotados com sucesso!")
        self.pause()

    def _format_eliminatory_result(self, result):
        """Format result for display in eliminatory tournaments."""
        if result == "1-0":
            return "Brancas avançam"
        elif result == "0-1":
            return "Pretas avançam"
        else:
            return None

    def _get_round_to_annotate(self, tournament):
        print("\nRodadas disponíveis:")
        for i, round_obj in enumerate(tournament.rounds, 1):
            print(f"{i} - Rodada {round_obj.round_}")
        
        round_choice = self.get_input("\nQual rodada deseja anotar? (ou 0 para voltar): ")

        if round_choice == '0':
            return None

        try:
            round_index = int(round_choice) - 1
            if 0 <= round_index < len(tournament.rounds):
                return tournament.rounds[round_index].round_
            else:
                self.display_error("Rodada inválida!")
                self.pause()
                return None
        except ValueError:
            self.display_error("Entrada inválida!")
            self.pause()
            return None

    def _annotate_matches_cursor_based(self, tournament, round_number, matches):
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

            for i, match in enumerate(matches):
                cursor = ">>>" if i == cursor_pos else "   "
                result_display = self._get_result_display(match.result)
                print(f"\n{cursor} Mesa {i+1}:{result_display}")
                print(f"    Brancas: {match.white.name}")
                if match.black is None:
                    print(f"    Pretas: BYE (vitória automática)")
                else:
                    print(f"    Pretas: {match.black.name}")

            command = self.get_input("\nComando: ").upper()

            if command in ['B', 'P', 'E']:
                self._update_match_result(tournament, round_number, cursor_pos, command, matches)
                matches = self.controller.get_round_matches(tournament.name, round_number)
                cursor_pos = min(cursor_pos + 1, len(matches) - 1)
            elif command == '' or command == '\n':
                cursor_pos = (cursor_pos + 1) % len(matches)
            elif command == 'Q':
                self.display_success("Resultados salvos com sucesso!")
                self.pause()
                break
            else:
                self.display_error("Comando inválido!")
                self.pause()

    def _get_result_display(self, result):
        if result == "1-0":
            return " [1-0]"
        elif result == "0-1":
            return " [0-1]"
        elif result == "0.5-0.5":
            return " [½-½]"
        else:
            return " [ - ]"

    def _update_match_result(self, tournament, round_number, cursor_pos, command, matches):
        result_map = {'B': "1-0", 'P': "0-1", 'E': "0.5-0.5"}
        if matches[cursor_pos].black is None:
            self.display_error("Esta partida já é BYE (vitória automática)!")
            self.pause()
        else:
            self.controller.update_match_result(
                tournament.name, 
                round_number, 
                cursor_pos, 
                result_map[command]
            )