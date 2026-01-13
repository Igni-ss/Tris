"""
Modulo per la gestione dell'Intelligenza Artificiale (Minimax).
"""
import math
from typing import Tuple

# Rimosso Optional che non era usato
from src.board import Board, EMPTY, PLAYER_O, PLAYER_X


def minimax(board: Board, depth: int, is_maximizing: bool) -> float:
    """
    Algoritmo Minimax ricorsivo.
    Restituisce un punteggio float (+10, -10, 0).
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
            board.grid[r][c] = EMPTY
            best_score = max(score, best_score)
        return best_score

    # RIMOSSO 'else' inutile: se l'if sopra fa return, qui ci arriviamo comunque.
    best_score = math.inf
    for r, c in board.get_available_moves():
        board.grid[r][c] = PLAYER_X
        score = minimax(board, depth + 1, True)
        board.grid[r][c] = EMPTY
        best_score = min(score, best_score)
    return best_score


def get_best_move(board: Board) -> Tuple[int, int]:
    """Calcola la mossa migliore per il PC."""
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