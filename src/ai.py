import math
from typing import Tuple, Optional
from src.board import Board, PLAYER_O, PLAYER_X, EMPTY


def minimax(board: Board, depth: int, is_maximizing: bool) -> float:
    """
    Algoritmo Minimax ricorsivo.

    Analizza l'albero delle mosse possibili per assegnare un punteggio allo stato attuale:
    +10: Vince il PC (O)
    -10: Vince l'Umano (X)
      0: Pareggio

    Il punteggio viene aggiustato con la 'depth' (profondità) per preferire
    vittorie veloci o sconfitte lente.
    """
    winner = board.check_winner()

    if winner == PLAYER_O:
        return 10 - depth
    if winner == PLAYER_X:
        return depth - 10
    if board.is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for r, c in board.get_available_moves():
            board.grid[r][c] = PLAYER_O
            score = minimax(board, depth + 1, False)
            board.grid[r][c] = EMPTY  # Backtracking
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for r, c in board.get_available_moves():
            board.grid[r][c] = PLAYER_X
            score = minimax(board, depth + 1, True)
            board.grid[r][c] = EMPTY  # Backtracking
            best_score = min(score, best_score)
        return best_score


def get_best_move(board: Board) -> Tuple[int, int]:
    """
    Determina la mossa migliore per il computer usando Minimax.
    """
    best_score = -math.inf
    best_move = (-1, -1)

    available_moves = board.get_available_moves()
    if len(available_moves) == 9:
        return (1, 1)

    for r, c in available_moves:
        board.grid[r][c] = PLAYER_O
        score = minimax(board, 0, False)
        board.grid[r][c] = EMPTY

        if score > best_score:
            best_score = score
            best_move = (r, c)

    return best_move
