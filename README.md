# ♟️ Chess Tournament Manager

Sistema completo de gerenciamento de torneios de xadrez desenvolvido em Python com arquitetura MVC (Model-View-Controller).

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Uso do Sistema](#uso-do-sistema)
- [Diagramas](#diagramas)
- [Contribuindo](#contribuindo)

## 🎯 Sobre o Projeto

O **Chess Tournament Manager** é um sistema robusto para gerenciamento de torneios de xadrez que suporta diferentes formatos de competição (Sistema Suíço e Eliminatório), múltiplos ritmos de jogo (Clássico, Rápido e Blitz), e fornece estatísticas avançadas de desempenho dos jogadores.

### Principais Diferenciais

- ✅ Suporte a torneios Swiss e Eliminatórios
- ✅ Sistema de emparceiramento automático com seeding
- ✅ Cálculo de Rating Performance e ganho estimado de rating
- ✅ Interface de console intuitiva com navegação por cursor
- ✅ Persistência de dados em JSON
- ✅ Validações completas de integridade de dados

## 🚀 Funcionalidades

### 1. Gerenciamento de Jogadores

- **Cadastro de Jogadores**
  - Nome, data de nascimento, gênero
  - Três ratings (Clássico, Rápido, Blitz)
  - Validação de dados com decorators
  
- **Listagem de Jogadores**
  - Ordenação alfabética
  - Visualização de todos os ratings

### 2. Gerenciamento de Torneios

#### Criação de Torneios
- Tipos: Swiss (N rodadas) ou Eliminatório (Chaves)
- Ritmos: Clássico, Rápido ou Blitz
- Configuração de local, datas e número de rodadas

#### Sistema Swiss
- Primeira rodada baseada em rating (top vs bottom half)
- Rodadas subsequentes baseadas em pontuação
- Número de rodadas configurável

#### Sistema Eliminatório
- Geração automática de chaves com seeding
- Suporte a BYEs para top seeds quando não há potência de 2
- Nomenclatura automática de rodadas (Quartas, Semifinal, Final)

### 3. Emparceiramento Inteligente

- **Sistema Swiss**: Pareamento baseado em pontuação e rating
- **Sistema Eliminatório**: Pareamento sequencial dos vencedores
- **Validação**: Todos os resultados devem estar anotados antes de gerar nova rodada
- **Menu Dinâmico**: Opção muda automaticamente entre "Gerar Emparceiramento" e "Anotar Resultados"

### 4. Anotação de Resultados

#### Para Torneios Swiss
```
Interface com cursor navegável:
- B: Brancas vencem (1-0)
- P: Pretas vencem (0-1)
- E: Empate (½-½)
- Enter: Próxima partida
- Q: Sair e salvar
```

#### Para Torneios Eliminatórios
```
Entrada de placar do match:
Exemplo: "2.5-1.5"
Sistema identifica automaticamente o vencedor
```

### 5. Sistema de Rankings

- **Ranking Inicial**: Baseado em rating do ritmo do torneio
- **Rankings por Rodada**: Após cada rodada completada
- **Estatísticas Completas**:
  - Pontuação e número de partidas
  - Vitórias/Empates/Derrotas
  - Rating médio dos adversários
  - Rating Performance (TPR)
  - Ganho estimado de rating

### 6. Cálculo de Estatísticas

#### Rating Performance
```
Fórmula: Performance Rating = Avg(Ratings Adversários) + dp

Onde dp é calculado baseado no percentual de pontos:
- dp = -400 × log₁₀((1-p)/p)

Casos especiais:
- 100% de pontos: PR = Avg + 400
- 50% de pontos: PR = Avg
- 0% de pontos: PR = Avg - 400
```

#### Ganho Estimado de Rating
```
Ganho = Performance Rating - Rating Atual

Exemplo:
Player: 2100 rating
Performance: 2300
Ganho estimado: +200 pontos
```

## 🏗️ Arquitetura

O projeto segue o padrão **MVC (Model-View-Controller)** com camadas bem definidas:

```
┌─────────────────────────────────────────────┐
│              PRESENTATION LAYER              │
│                   (Views)                    │
│  - MainView, PlayerView, TournamentView     │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│              BUSINESS LAYER                  │
│                (Controllers)                 │
│  - PlayerController, TournamentController   │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│              DATA LAYER                      │
│                  (DTOs)                      │
│      - PlayerDTO, TournamentDTO              │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│              DOMAIN LAYER                    │
│                 (Entities)                   │
│  - Player, Tournament, Round, Game, etc.    │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│              PERSISTENCE LAYER               │
│                  (JSON)                      │
│      - players.json, tournaments.json        │
└─────────────────────────────────────────────┘
```

### Responsabilidades das Camadas

- **Views**: Interface com usuário, captura de entrada, exibição de dados
- **Controllers**: Lógica de negócio, validações, orquestração
- **DTOs**: Serialização/deserialização de dados
- **Entities**: Modelos de domínio com regras de negócio
- **Persistence**: Armazenamento e recuperação de dados

## 💻 Tecnologias Utilizadas

- **Python 3.10+**
  - Type hints para tipagem estática
  - Decorators para validação
  - Enums para constantes
  
- **Padrões de Design**
  - MVC (Model-View-Controller)
  - DTO (Data Transfer Object)
  - Repository Pattern
  - Factory Pattern (para criação de torneios)
  
- **Armazenamento**
  - JSON para persistência de dados
  - Encoding UTF-8 para suporte a caracteres especiais

## 📁 Estrutura do Projeto

```
chess-tournament-manager/
│
├── main.py                          # Ponto de entrada do sistema
│
├── src/
│   ├── entities/                    # Modelos de domínio
│   │   ├── player.py               # Entidade Player
│   │   ├── rating.py               # Entidade Rating
│   │   ├── tournament.py           # Classe base Tournament
│   │   ├── swiss_tournament.py     # Torneio Swiss
│   │   ├── eliminatory_tournament.py # Torneio Eliminatório
│   │   ├── round.py                # Entidade Round
│   │   ├── game.py                 # Entidade Game
│   │   └── time_control.py         # Enum TimeControl
│   │
│   ├── controllers/                 # Lógica de negócio
│   │   ├── base_controller.py      # Controller base
│   │   ├── player_controller.py    # Controller de jogadores
│   │   └── tournament_controller.py # Controller de torneios
│   │
│   ├── views/                       # Interface com usuário
│   │   ├── base_view.py            # View base
│   │   ├── main_view.py            # Menu principal
│   │   ├── player_view.py          # Views de jogadores
│   │   └── tournament_view.py      # Views de torneios
│   │
│   ├── dtos/                        # Data Transfer Objects
│   │   ├── player_dto.py           # DTO de Player
│   │   └── tournament_dto.py       # DTO de Tournament
│   │
│   ├── utils/                       # Utilitários
│   │   └── decorators.py           # Decorators de validação
│   │
│   └── data/                        # Armazenamento JSON
│       ├── players.json            # Dados de jogadores
│       └── tournaments.json        # Dados de torneios
│
├── tests/                           # Scripts de teste
│   ├── test_rounds_save.py
│   ├── test_eliminatory_flow.py
│   └── test_player_statistics.py
│
├── README.md                        # Este arquivo
├── FUNCIONALIDADES.md              # Documentação detalhada
└── UML_DIAGRAM.md                  # Diagrama UML de classes
```

## 🔧 Como Executar

### Pré-requisitos

- Python 3.10 ou superior
- Sistema operacional: Windows, Linux ou macOS

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/chess-tournament-manager.git
cd chess-tournament-manager
```

2. Execute o sistema:
```bash
python main.py
```

Não há dependências externas! O projeto usa apenas a biblioteca padrão do Python.

## 📖 Uso do Sistema

### Fluxo Básico - Torneio Swiss

1. **Cadastrar Jogadores**
   ```
   Menu Principal → 1 - Jogador → 1 - Cadastrar jogador
   ```

2. **Criar Torneio**
   ```
   Menu Principal → 2 - Torneio → 1 - Criar novo torneio
   Escolher: Tipo Swiss, Ritmo desejado, Número de rodadas
   ```

3. **Adicionar Jogadores ao Torneio**
   ```
   2 - Torneio → 3 - Gerenciar torneio → Selecionar torneio
   2 - Adicionar jogador (repetir para cada jogador)
   ```

4. **Gerar Emparceiramento**
   ```
   6 - Gerar emparceiramento (1ª rodada)
   ```

5. **Anotar Resultados**
   ```
   6 - Anotar resultados (após partidas)
   Usar B (brancas), P (pretas), E (empate), Q (sair)
   ```

6. **Ver Rankings**
   ```
   4 - Ver rankings → Escolher rodada
   ```

7. **Repetir** passos 4-6 para cada rodada

### Fluxo Básico - Torneio Eliminatório

1-3. Igual ao Swiss

4. **Gerar Chave**
   ```
   6 - Gerar emparceiramento (1ª rodada)
   Sistema cria chave com seeding automático
   ```

5. **Anotar Placares**
   ```
   6 - Anotar resultados
   Digitar placar: ex: "2.5-1.5"
   ```

6. **Gerar Próxima Fase**
   ```
   6 - Gerar emparceiramento (2ª rodada)
   Sistema emparelha vencedores automaticamente
   ```

7. **Repetir** até a Final

## 📊 Diagramas

### Diagrama UML de Classes

Veja o arquivo [UML_DIAGRAM.md](UML_DIAGRAM.md) para o diagrama completo de classes do sistema.

### Fluxo de Dados

```
[User Input] → [View] → [Controller] → [Entity]
                  ↑          ↓            ↓
                  ←──── [DTO] ←──── [JSON]
```

## 🎯 Casos de Uso

### UC01: Cadastrar Jogador
**Ator**: Organizador  
**Fluxo**:
1. Seleciona opção de cadastrar jogador
2. Informa nome, data de nascimento, gênero
3. Informa ratings (clássico, rápido, blitz)
4. Sistema valida e salva

### UC02: Criar Torneio
**Ator**: Organizador  
**Fluxo**:
1. Seleciona criar torneio
2. Escolhe tipo (Swiss/Eliminatório)
3. Informa nome, local, datas, ritmo
4. Para Swiss: informa número de rodadas
5. Sistema valida e cria torneio

### UC03: Gerar Emparceiramento
**Ator**: Organizador  
**Pré-condição**: Torneio tem jogadores suficientes  
**Fluxo**:
1. Seleciona opção de gerar emparceiramento
2. Sistema valida resultados da rodada anterior
3. Sistema gera pairings baseado no algoritmo
4. Sistema exibe pairings para confirmação
5. Organizador confirma
6. Sistema salva rodada

### UC04: Anotar Resultados
**Ator**: Organizador  
**Pré-condição**: Rodada foi gerada  
**Fluxo**:
1. Seleciona rodada a anotar
2. Para cada partida, informa resultado
3. Sistema valida e salva
4. Sistema atualiza estatísticas

### UC05: Visualizar Rankings
**Ator**: Organizador/Jogador  
**Fluxo**:
1. Seleciona opção de rankings
2. Escolhe rodada (inicial ou após rodada N)
3. Sistema calcula rankings
4. Sistema exibe com estatísticas completas

## 🔒 Validações Implementadas

- ✅ Validação de tipos com decorators
- ✅ Validação de datas (formato YYYY-MM-DD)
- ✅ Validação de gênero (M/F)
- ✅ Validação de ratings (valores positivos)
- ✅ Validação de resultados (formatos válidos)
- ✅ Validação de pré-requisitos para gerar rodadas
- ✅ Validação de unicidade de nomes (jogadores e torneios)

## 🐛 Tratamento de Erros

O sistema possui tratamento robusto de erros:
- Mensagens de erro claras e descritivas
- Rollback automático em caso de falha
- Validação antes de operações críticas
- Logs de exceções para debugging

## 📈 Melhorias Futuras

- [ ] Interface gráfica (GUI com Tkinter/PyQt)
- [ ] Exportação de relatórios (PDF/Excel)
- [ ] Sistema de autenticação de usuários
- [ ] Banco de dados SQL para melhor performance
- [ ] API REST para integração
- [ ] Sistema de desempate Buchholz/Sonneborn-Berger
- [ ] Impressão de tabelas de jogos
- [ ] Sistema de notificações por e-mail
- [ ] Integração com FIDE para ratings oficiais

## 👨‍💻 Autor

**Gustavo Kayser**  
Estudante de Programação Orientada a Objetos  
Universidade Federal do Paraná

## 📄 Licença

Este projeto é de código aberto e está disponível para fins educacionais.

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Entre em contato pelo e-mail: gustavo@example.com

---

**Desenvolvido com ♟️ e Python**
