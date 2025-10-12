# 📐 Diagrama UML de Classes - Chess Tournament Manager

## Diagrama Completo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ENTITY LAYER (DOMAIN)                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────┐
│        <<enum>>            │
│      TimeControl           │
├────────────────────────────┤
│ + CLASSIC: str             │
│ + RAPID: str               │
│ + BLITZ: str               │
├────────────────────────────┤
│ + from_string(value: str)  │
│   : TimeControl            │
│ + __str__(): str           │
└────────────────────────────┘

┌────────────────────────────┐
│         Rating             │
├────────────────────────────┤
│ - __classic: int           │
│ - __rapid: int             │
│ - __blitz: int             │
├────────────────────────────┤
│ + __init__(classic, rapid, │
│   blitz)                   │
│ + classic: int {get, set}  │
│ + rapid: int {get, set}    │
│ + blitz: int {get, set}    │
└────────────────────────────┘
         △
         │ has
         │
┌────────────────────────────┐
│         Player             │
├────────────────────────────┤
│ - __name: str              │
│ - __birthdate: str         │
│ - __gender: str            │
│ - __rating: Rating         │
├────────────────────────────┤
│ + __init__(name, birthdate,│
│   gender, rating)          │
│ + name: str {get, set}     │
│ + birthdate: str {get, set}│
│ + gender: str {get, set}   │
│ + rating: Rating {get, set}│
└────────────────────────────┘
         △
         │ plays in
         │
┌────────────────────────────┐          ┌────────────────────────────┐
│         Game               │          │         Round              │
├────────────────────────────┤          ├────────────────────────────┤
│ - __white: Player          │◄─────────│ - __round: int             │
│ - __black: Player | None   │ contains │ - __subround: int          │
│ - __result: str | None     │   many   │ - __matches: list[Game]    │
├────────────────────────────┤          ├────────────────────────────┤
│ + __init__(white, black)   │          │ + __init__(round_, subround│
│ + white: Player {get, set} │          │ + round_: int {get, set}   │
│ + black: Player {get, set} │          │ + subround: int {get, set} │
│ + result: str {get, set}   │          │ + matches: list {get, set} │
│   Valid: "1-0", "0-1",     │          │ + add_match(game: Game)    │
│          "0.5-0.5"         │          │ + get_match_count(): int   │
└────────────────────────────┘          └────────────────────────────┘
                                                   △
                                                   │ contains
                                                   │ many
                                         ┌─────────────────────┐
                                         │                     │
                              ┌──────────────────────────────────────────┐
                              │            Tournament                    │
                              │              <<abstract>>                │
                              ├──────────────────────────────────────────┤
                              │ - __name: str                            │
                              │ - __location: str                        │
                              │ - __start_date: str                      │
                              │ - __end_date: str                        │
                              │ - __time_control: TimeControl            │
                              │ - __players: list[Player]                │
                              │ - __rounds: list[Round]                  │
                              ├──────────────────────────────────────────┤
                              │ + __init__(name, location, start_date,   │
                              │   end_date, time_control)                │
                              │ + name: str {get, set}                   │
                              │ + location: str {get, set}               │
                              │ + start_date: str {get, set}             │
                              │ + end_date: str {get, set}               │
                              │ + time_control: TimeControl {get, set}   │
                              │ + players: list[Player] {get}            │
                              │ + rounds: list[Round] {get}              │
                              │ + add_player(player: Player)             │
                              │ + remove_player(player_name: str): bool  │
                              │ + get_player_by_name(name: str): Player  │
                              │ + get_players_by_rating(rating_type: str)│
                              │   : list[Player]                         │
                              │ + add_round(round_obj: Round)            │
                              │ + get_round(round_number: int): Round    │
                              │ + get_current_round_number(): int        │
                              └──────────────────────────────────────────┘
                                         △                    △
                                         │                    │
                           ┌─────────────┴──────┐    ┌───────┴──────────────┐
                           │                    │    │                      │
                  ┌────────────────────┐   ┌───────────────────────────┐
                  │  SwissTournament   │   │  EliminatoryTournament    │
                  ├────────────────────┤   ├───────────────────────────┤
                  │ - __num_rounds: int│   │                           │
                  ├────────────────────┤   ├───────────────────────────┤
                  │ + __init__(name,   │   │ + __init__(name,          │
                  │   location,        │   │   location, start_date,   │
                  │   start_date,      │   │   end_date, time_control) │
                  │   end_date,        │   │ + generate_bracket_       │
                  │   time_control,    │   │   pairings(round_number)  │
                  │   num_rounds)      │   │   : list[tuple]           │
                  │ + num_rounds: int  │   │ + get_bracket_info(): dict│
                  │   {get, set}       │   │ - _get_match_winner(match)│
                  │ + generate_swiss_  │   │   : Player | None         │
                  │   pairings(round_  │   │                           │
                  │   number): list    │   │                           │
                  │   [tuple]          │   │                           │
                  └────────────────────┘   └───────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           CONTROLLER LAYER                                   │
└─────────────────────────────────────────────────────────────────────────────┘

                         ┌────────────────────────────┐
                         │     BaseController         │
                         │      <<abstract>>          │
                         ├────────────────────────────┤
                         │ - filename: str            │
                         ├────────────────────────────┤
                         │ # _load_data(): list       │
                         │ # _save_data(data: list)   │
                         └────────────────────────────┘
                                      △
                                      │ extends
                      ┌───────────────┴─────────────────┐
                      │                                 │
         ┌────────────────────────┐      ┌──────────────────────────────┐
         │  PlayerController      │      │  TournamentController        │
         ├────────────────────────┤      ├──────────────────────────────┤
         │ - filename: str        │      │ - filename: str              │
         ├────────────────────────┤      ├──────────────────────────────┤
         │ + __init__()           │      │ + __init__()                 │
         │ + register_player(     │      │ + create_tournament(         │
         │   player: Player)      │      │   tournament: Tournament)    │
         │ + get_all_players()    │      │ + get_all_tournaments()      │
         │   : list[Player]       │      │   : list[Tournament]         │
         │ + get_player_by_name(  │      │ + get_tournament_by_name(    │
         │   name: str): Player   │      │   name: str): Tournament     │
         │ + list_players(): list │      │ + list_tournaments(): list   │
         │ + update_player(       │      │ + update_tournament(name,    │
         │   old_name, player)    │      │   tournament)                │
         │ + delete_player(       │      │ + delete_tournament(name)    │
         │   name: str): bool     │      │ + add_player_to_tournament(  │
         │                        │      │   tournament_name,           │
         │                        │      │   player_name)               │
         │                        │      │ + remove_player_from_        │
         │                        │      │   tournament(tournament_name,│
         │                        │      │   player_name)               │
         │                        │      │ + get_tournament_ranking(    │
         │                        │      │   tournament_name,           │
         │                        │      │   rating_type): list         │
         │                        │      │ + generate_round_pairings(   │
         │                        │      │   tournament_name): list     │
         │                        │      │ + save_round_pairings(       │
         │                        │      │   tournament_name, round_num,│
         │                        │      │   pairings)                  │
         │                        │      │ + get_bracket_info(          │
         │                        │      │   tournament_name): dict     │
         │                        │      │ + get_round_matches(         │
         │                        │      │   tournament_name, round_num)│
         │                        │      │   : list[Game]               │
         │                        │      │ + update_match_result(       │
         │                        │      │   tournament_name, round_num,│
         │                        │      │   match_index, result)       │
         │                        │      │ + get_player_statistics(     │
         │                        │      │   tournament_name,           │
         │                        │      │   player_name): dict         │
         │                        │      │ + get_all_players_statistics(│
         │                        │      │   tournament_name): list     │
         └────────────────────────┘      └──────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              DTO LAYER                                       │
└─────────────────────────────────────────────────────────────────────────────┘

         ┌────────────────────────┐      ┌──────────────────────────────┐
         │     PlayerDTO          │      │     TournamentDTO            │
         ├────────────────────────┤      ├──────────────────────────────┤
         │ <<static>>             │      │ <<static>>                   │
         ├────────────────────────┤      ├──────────────────────────────┤
         │ + to_dict(player:      │      │ + to_dict(tournament:        │
         │   Player): dict        │      │   Tournament): dict          │
         │ + from_dict(data: dict)│      │ + from_dict(data: dict)      │
         │   : Player             │      │   : Tournament               │
         └────────────────────────┘      │ - _game_to_dict(game: Game)  │
                                         │   : dict                     │
                                         │ - _game_from_dict(data: dict)│
                                         │   : Game                     │
                                         │ - _round_to_dict(round: Round│
                                         │   : dict                     │
                                         │ - _round_from_dict(data: dict│
                                         │   : Round                    │
                                         └──────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              VIEW LAYER                                      │
└─────────────────────────────────────────────────────────────────────────────┘

                         ┌────────────────────────────┐
                         │       BaseView             │
                         │      <<abstract>>          │
                         ├────────────────────────────┤
                         │ <<static>>                 │
                         ├────────────────────────────┤
                         │ + clear_screen()           │
                         │ + display_separator()      │
                         │ + display_message(msg: str)│
                         │ + display_error(msg: str)  │
                         │ + display_success(msg: str)│
                         │ + get_input(prompt: str)   │
                         │   : str                    │
                         │ + pause()                  │
                         └────────────────────────────┘
                                      △
                                      │ extends
                      ┌───────────────┴─────────────────┐
                      │                                 │
         ┌────────────────────────┐      ┌──────────────────────────────┐
         │     PlayerView         │      │     TournamentView           │
         ├────────────────────────┤      ├──────────────────────────────┤
         │ - controller:          │      │ - controller:                │
         │   PlayerController     │      │   TournamentController       │
         │                        │      │ - player_controller:         │
         │                        │      │   PlayerController           │
         ├────────────────────────┤      ├──────────────────────────────┤
         │ + __init__()           │      │ + __init__()                 │
         │ + show_menu()          │      │ + show_menu()                │
         │ - _register_player()   │      │ - create_tournament_screen() │
         │ - _list_players()      │      │ - list_tournaments_screen()  │
         │                        │      │ - manage_tournament_screen() │
         │                        │      │ - _manage_tournament_menu(   │
         │                        │      │   tournament)                │
         │                        │      │ - _can_generate_next_round(  │
         │                        │      │   tournament): bool          │
         │                        │      │ - _view_tournament_details(  │
         │                        │      │   tournament)                │
         │                        │      │ - _add_player_to_tournament( │
         │                        │      │   tournament)                │
         │                        │      │ - _remove_player_from_       │
         │                        │      │   tournament(tournament)     │
         │                        │      │ - _view_rankings_menu(       │
         │                        │      │   tournament)                │
         │                        │      │ - _view_tournament_ranking(  │
         │                        │      │   tournament, is_initial)    │
         │                        │      │ - _view_round_ranking(       │
         │                        │      │   tournament, round_number)  │
         │                        │      │ - _list_tournament_players(  │
         │                        │      │   tournament)                │
         │                        │      │ - _generate_round_pairings(  │
         │                        │      │   tournament)                │
         │                        │      │ - _annotate_results(         │
         │                        │      │   tournament)                │
         │                        │      │ - _annotate_swiss_matches(   │
         │                        │      │   tournament, round_number,  │
         │                        │      │   matches)                   │
         │                        │      │ - _annotate_eliminatory_     │
         │                        │      │   matches(tournament,        │
         │                        │      │   round_number, matches)     │
         │                        │      │ - _edit_tournament(          │
         │                        │      │   tournament)                │
         │                        │      │ - _delete_tournament(        │
         │                        │      │   tournament): bool          │
         └────────────────────────┘      └──────────────────────────────┘
                      │                                 │
                      │ uses                            │ uses
                      └─────────────┬───────────────────┘
                                    │
                         ┌────────────────────────────┐
                         │       MainView             │
                         ├────────────────────────────┤
                         │ - player_view: PlayerView  │
                         │ - tournament_view:         │
                         │   TournamentView           │
                         ├────────────────────────────┤
                         │ + __init__()               │
                         │ + run()                    │
                         │ + show_main_menu()         │
                         └────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            UTILITY LAYER                                     │
└─────────────────────────────────────────────────────────────────────────────┘

                         ┌────────────────────────────┐
                         │     type_check             │
                         │     <<decorator>>          │
                         ├────────────────────────────┤
                         │ Validates parameter types  │
                         │ using type hints           │
                         └────────────────────────────┘
```

## Relacionamentos Principais

### 1. Herança (Generalização/Especialização)

```
BaseController ◄─── PlayerController
               ◄─── TournamentController

BaseView ◄─── PlayerView
         ◄─── TournamentView
         ◄─── MainView

Tournament ◄─── SwissTournament
           ◄─── EliminatoryTournament
```

### 2. Composição (Parte-Todo)

```
Player ◄──● Rating
       (Player possui um Rating)

Tournament ◄──● Player (many)
           (Tournament possui múltiplos Players)

Tournament ◄──● Round (many)
           (Tournament possui múltiplos Rounds)

Round ◄──● Game (many)
      (Round possui múltiplos Games)

Game ◄──● Player (white)
     ◄──● Player (black, opcional)
     (Game possui dois Players)
```

### 3. Associação

```
PlayerController ──► PlayerDTO
                 ──► Player

TournamentController ──► TournamentDTO
                     ──► Tournament
                     ──► Round
                     ──► Game

PlayerView ──► PlayerController

TournamentView ──► TournamentController
               ──► PlayerController

MainView ──► PlayerView
         ──► TournamentView
```

### 4. Dependência

```
SwissTournament ···► Player (para gerar pairings)

EliminatoryTournament ···► Player (para gerar bracket)

TournamentDTO ···► PlayerDTO (para serialização)
```

## Padrões de Design Aplicados

### 1. **MVC (Model-View-Controller)**
- **Model**: Entities (Player, Tournament, Round, Game)
- **View**: Views (MainView, PlayerView, TournamentView)
- **Controller**: Controllers (PlayerController, TournamentController)

### 2. **DTO (Data Transfer Object)**
- PlayerDTO e TournamentDTO para serialização/deserialização

### 3. **Template Method**
- BaseController define estrutura de load/save
- Subclasses implementam lógica específica

### 4. **Factory Method**
- TournamentDTO.from_dict() cria instâncias corretas baseado no tipo

### 5. **Strategy**
- SwissTournament e EliminatoryTournament com algoritmos diferentes

### 6. **Decorator**
- @type_check para validação de tipos

## Multiplicidades

```
Tournament "1" ──── "*" Player
Tournament "1" ──── "*" Round
Round "1" ──── "*" Game
Game "1" ──── "1" Player (white)
Game "1" ──── "0..1" Player (black)
Player "1" ──── "1" Rating
```

## Diagrama de Sequência - Gerar Emparceiramento

```
┌──────┐      ┌──────────────┐      ┌─────────────────────┐      ┌────────────┐
│ User │      │TournamentView│      │TournamentController│      │ Tournament │
└──┬───┘      └──────┬───────┘      └──────────┬──────────┘      └─────┬──────┘
   │                 │                          │                       │
   │  6-Gerar        │                          │                       │
   │  Emparceiramento│                          │                       │
   │────────────────>│                          │                       │
   │                 │                          │                       │
   │                 │ generate_round_pairings()│                       │
   │                 │─────────────────────────>│                       │
   │                 │                          │                       │
   │                 │                          │ get_current_round_   │
   │                 │                          │ number()              │
   │                 │                          │──────────────────────>│
   │                 │                          │<──────────────────────│
   │                 │                          │ round_number          │
   │                 │                          │                       │
   │                 │                          │ generate_swiss_      │
   │                 │                          │ pairings() ou        │
   │                 │                          │ generate_bracket_    │
   │                 │                          │ pairings()           │
   │                 │                          │──────────────────────>│
   │                 │                          │<──────────────────────│
   │                 │                          │ pairings              │
   │                 │<─────────────────────────│                       │
   │                 │ pairings                 │                       │
   │                 │                          │                       │
   │  [Exibir        │                          │                       │
   │   Pairings]     │                          │                       │
   │<────────────────│                          │                       │
   │                 │                          │                       │
   │  Confirmar (S)  │                          │                       │
   │────────────────>│                          │                       │
   │                 │                          │                       │
   │                 │ save_round_pairings()    │                       │
   │                 │─────────────────────────>│                       │
   │                 │                          │                       │
   │                 │                          │ add_round()          │
   │                 │                          │──────────────────────>│
   │                 │                          │                       │
   │                 │                          │ update_tournament()  │
   │                 │                          │──────────────────────>│
   │                 │<─────────────────────────│                       │
   │                 │ success                  │                       │
   │  [Sucesso!]     │                          │                       │
   │<────────────────│                          │                       │
   │                 │                          │                       │
```

## Diagrama de Sequência - Calcular Estatísticas

```
┌──────┐      ┌──────────────┐      ┌─────────────────────┐      ┌────────────┐
│ User │      │TournamentView│      │TournamentController│      │ Tournament │
└──┬───┘      └──────┬───────┘      └──────────┬──────────┘      └─────┬──────┘
   │                 │                          │                       │
   │  5-Listar       │                          │                       │
   │  Jogadores      │                          │                       │
   │────────────────>│                          │                       │
   │                 │                          │                       │
   │                 │ loop [for each player]   │                       │
   │                 │─┐                        │                       │
   │                 │ │                        │                       │
   │                 │ │get_player_statistics() │                       │
   │                 │ │───────────────────────>│                       │
   │                 │ │                        │                       │
   │                 │ │                        │ rounds                │
   │                 │ │                        │──────────────────────>│
   │                 │ │                        │<──────────────────────│
   │                 │ │                        │                       │
   │                 │ │                        │ loop [for each round] │
   │                 │ │                        │─┐                     │
   │                 │ │                        │ │ matches             │
   │                 │ │                        │ │────────────────────>│
   │                 │ │                        │ │<────────────────────│
   │                 │ │                        │ │                     │
   │                 │ │                        │ │ [calculate points,  │
   │                 │ │                        │ │  opponent ratings,  │
   │                 │ │                        │ │  performance]       │
   │                 │ │                        │<┘                     │
   │                 │ │                        │                       │
   │                 │ │<───────────────────────│                       │
   │                 │ │ statistics             │                       │
   │                 │<┘                        │                       │
   │                 │                          │                       │
   │  [Exibir        │                          │                       │
   │   Estatísticas] │                          │                       │
   │<────────────────│                          │                       │
   │                 │                          │                       │
```

## Notas de Implementação

### Validações com Decorators
O decorator `@type_check` valida tipos de parâmetros automaticamente usando type hints.

### Persistência
- Dados salvos em JSON com encoding UTF-8
- DTOs responsáveis por serialização/deserialização
- Controllers gerenciam operações de I/O

### Algoritmos de Pairing

**Swiss System**:
1. Primeira rodada: Top half vs Bottom half ordenado por rating
2. Rodadas seguintes: Baseado em pontuação (simplificado)

**Eliminatory System**:
1. Primeira rodada: Seeding com BYEs para top players
2. Rodadas seguintes: Vencedores emparelhados sequencialmente

### Cálculo de Performance Rating

```python
if percentage == 1.0:
    performance = avg_opponent_rating + 400
elif percentage == 0.0:
    performance = avg_opponent_rating - 400
else:
    dp = -400 * log10((1 - percentage) / percentage)
    performance = avg_opponent_rating + dp
```

---

**Este diagrama representa a arquitetura completa do sistema Chess Tournament Manager**
