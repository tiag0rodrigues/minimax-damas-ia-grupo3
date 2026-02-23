# Algoritmo Minimax com Poda Alfa-Beta
import math

"""
Função principal chamada pela IA.
game  -> objeto que contém as regras do jogo
state -> estado atual do tabuleiro
depth -> profundidade máxima da busca (quanto maior, mais inteligente, porém mais lento)
"""


def ALPHA_BETA_SEARCH(game, state, depth=6):
    player = game.TO_MOVE(state)
    value, move = MAX_VALUE(game, state, -math.inf, math.inf, player, depth)
    return move


"""
MAX tenta maximizar o valor da jogada.
Representa o turno da IA (ou jogador principal).
"""


def MAX_VALUE(game, state, alpha, beta, player, depth):
    if game.IS_TERMINAL(state) or depth == 0:
        return game.UTILITY(state, player), None

    v = -math.inf
    best_move = None

    for action in game.ACTIONS(state):
        v2, _ = MIN_VALUE(game, game.RESULT(state, action),
                          alpha, beta, player, depth-1)
        if v2 > v:
            v = v2
            best_move = action
            alpha = max(alpha, v)

        if v >= beta:
            return v, best_move

    return v, best_move


"""
MIN tenta minimizar o valor.
Representa o turno do adversário.
"""


def MIN_VALUE(game, state, alpha, beta, player, depth):
    if game.IS_TERMINAL(state) or depth == 0:
        return game.UTILITY(state, player), None

    v = math.inf
    best_move = None

    for action in game.ACTIONS(state):
        # Simula a jogada e chama MAX novamente
        v2, _ = MAX_VALUE(game, game.RESULT(state, action),
                          alpha, beta, player, depth-1)
        if v2 < v:      # Se encontramos valor menor, atualizamos
            v = v2
            best_move = action
            # Atualiza beta (melhor valor garantido para MIN)
            beta = min(beta, v)

        # Se o valor atual já é menor ou igual ao alpha,
        # MAX nunca deixará esse ramo acontecer,
        # então podemos cortar aqui.
        if v <= alpha:
            return v, best_move

    return v, best_move
