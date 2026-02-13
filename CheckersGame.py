import copy

# -------------------------
# Representação do jogo da DAMA INGLESA
# -------------------------
# Tabuleiro
# 'b' = peça preta (MAX) - só andam e capturam para frente
# 'w' = peça branca (MIN) - só andam e capturam para frente
# 'B' = dama preta - andam e capturam para frente e para trás 1 casa por vez
# 'W' = dama branca - andam e capturam para frente e para trás 1 casa por vez
# '.' = vazio
# -----------------------
# Outras regras
# A captura é obrigatória
# Se houver mais de uma captura disponível com a mesma peça, tem que realizar todas as capturas
# O jogo termina quando todas as peças do adversário são capturadas ou quando há um empate (repetição)

class CheckersGame:
    def __init__(self, size=4):
        self.size = size
        self.capture = None

    def TO_MOVE(self, state):
        return state["player"]
    
    def _state_key(self, state):
        board_key = tuple(tuple(row) for row in state["board"])
        return (board_key, state["player"])

    def ACTIONS(self, state):
        board = state["board"]
        player = state["player"]
        captures = []
        moves = []

        for r in range(self.size):
            for c in range(self.size):
                piece = board[r][c]
                if piece.lower() != player:
                    continue

                is_king = piece.isupper()
                # Direções: Pretas (b) descem (+1), Brancas (w) sobem (-1). Damas fazem ambos.
                directions = [1, -1] if is_king else ([1] if player == "b" else [-1])

                for dr in directions:
                    for dc in [-1, 1]:
                        # 1. Verificar Captura (Salto)
                        nr, nc = r + 2 * dr, c + 2 * dc
                        if 0 <= nr < self.size and 0 <= nc < self.size:
                            action = ((r, c), (nr, nc))
                            if self.IS_VALID_ACTION(state, action):
                                # Verifica se continua de outra captura
                                if self.capture is not None and self.capture["player"] == player:
                                    (r1, c1), (r2, c2) = self.capture["action"]
                                    if r == r2 and c == c2:
                                        self.capture = None
                                        return [action] #retorna a única jogada permitida
                                captures.append(action)
                        
                        # 2. Verificar Movimento Simples
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.size and 0 <= nc < self.size:
                            action = ((r, c), (nr, nc))
                            if self.IS_VALID_ACTION(state, action):
                                moves.append(action)
        # Força captura
        return captures if captures else moves

    def RESULT(self, state, action):
        board = copy.deepcopy(state["board"])
        player = state["player"]
        
        # Salva histórico ANTES de mudar o estado para detectar repetição futura
        history = state.get("history", set()).copy()
        history.add(self._state_key(state))

        (r1, c1), (r2, c2) = action
        piece = board[r1][c1]
        
        # Move a peça
        board[r1][c1] = "."
        
        # Lógica de Captura: remove a peça do meio
        if abs(r2 - r1) == 2:
            board[(r1 + r2) // 2][(c1 + c2) // 2] = "."

        # Promoção para Dama
        if piece == "b" and r2 == self.size - 1:
            piece = "B"
        elif piece == "w" and r2 == 0:
            piece = "W"
            
        board[r2][c2] = piece

        #verifica se há outra captura a ser feita após captura
        new_state = {
            "board": board,
            "player": player,
            "history": history
        }
        actions = self.ACTIONS(new_state)
        next_player = "."
        if abs(r2 - r1) == 2 and actions:
            for act in actions:
                (source_r, source_c), (dest_r, dest_c) = act
                dr, dc =  dest_r - source_r, dest_c - source_c
                if abs(dr) == 2 and abs(dc) == 2:
                    if source_r == r2 and source_c == c2:
                        next_player = player # jogador continua jogada
                        self.capture = { # guarda captura
                            "player": next_player,
                            "action": action
                        }
                        break

        if next_player == ".":
            next_player = "w" if player == "b" else "b"

        return {
            "board": board,
            "player": next_player,
            "history": history,
        }

    def IS_TERMINAL(self, state):
        # Se alguém não tem peças
        board = state["board"]
        b_pieces = sum(cell.lower() == "b" for row in board for cell in row)
        w_pieces = sum(cell.lower() == "w" for row in board for cell in row)
        if b_pieces == 0 or w_pieces == 0: return True

        # Se o jogador atual não tem movimentos
        if not self.ACTIONS(state): return True
        
        # Empate por repetição
        if self._state_key(state) in state.get("history", set()): return True

        return False

    def UTILITY(self, state, player):
        # Se terminal por repetição
        if self._state_key(state) in state.get("history", set()):
            return 0
        
        board = state["board"]
        b_score = sum((1 if c == 'b' else 3 if c == 'B' else 0) for r in board for c in r)
        w_score = sum((1 if c == 'w' else 3 if c == 'W' else 0) for r in board for c in r)

        if player == "b":
            return b_score - w_score
        else:
            return w_score - b_score

    def IS_VALID_ACTION(self, state, action):
        board = state["board"]
        player = state["player"]
        opponent = "w" if player == "b" else "b"
        (r1, c1), (r2, c2) = action

        # Validações básicas de limite e ocupação
        if not (0 <= r2 < self.size and 0 <= c2 < self.size): return False
        if board[r2][c2] != ".": return False
        
        piece = board[r1][c1]
        is_king = piece.isupper()
        dr, dc = r2 - r1, c2 - c1

        # Movimento Simples (Diferença de 1 linha)
        if abs(dr) == 1 and abs(dc) == 1:
            if is_king: return True
            return dr == (1 if player == "b" else -1)

        # Captura (Diferença de 2 linhas)
        if abs(dr) == 2 and abs(dc) == 2:
            mid_r, mid_c = (r1 + r2) // 2, (c1 + c2) // 2
            mid_piece = board[mid_r][mid_c]
            if mid_piece != "." and mid_piece.lower() == opponent:
                if is_king: return True
                return dr == (2 if player == "b" else -2)

        return False