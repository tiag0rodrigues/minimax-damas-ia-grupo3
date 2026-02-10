# Algoritmo Minimax com Poda Alfa-Beta
import math

def ALPHA_BETA_SEARCH(game, state, depth=6):
    player = game.TO_MOVE(state)
    value, move = MAX_VALUE(game, state, -math.inf, math.inf, player, depth)
    return move


def MAX_VALUE(game, state, alpha, beta, player, depth):
    if game.IS_TERMINAL(state) or depth == 0:
        return game.UTILITY(state, player), None

    v = -math.inf
    best_move = None

    for action in game.ACTIONS(state):
        v2, _ = MIN_VALUE(game, game.RESULT(state, action), alpha, beta, player, depth-1)
        if v2 > v:
            v = v2
            best_move = action
            alpha = max(alpha, v)

        if v >= beta:
            return v, best_move

    return v, best_move


def MIN_VALUE(game, state, alpha, beta, player, depth):
    if game.IS_TERMINAL(state) or depth == 0:
        return game.UTILITY(state, player), None

    v = math.inf
    best_move = None

    for action in game.ACTIONS(state):
        v2, _ = MAX_VALUE(game, game.RESULT(state, action), alpha, beta, player, depth-1)
        if v2 < v:
            v = v2
            best_move = action
            beta = min(beta, v)

        if v <= alpha:
            return v, best_move

    return v, best_move