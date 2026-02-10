"""Modulo di test per l'algoritmo Minimax dell'IA."""

import pytest
from src.modules.ai import get_best_move
from src.modules.board import EMPTY, PLAYER_O, PLAYER_X, Board

SCENARIOS = [
    {
        "name": "Vittoria immediata PC",
        "grid": [
            [PLAYER_O, PLAYER_O, EMPTY],
            [EMPTY, PLAYER_X, EMPTY],
            [EMPTY, EMPTY, PLAYER_X],
        ],
        "expected": (0, 2),
    },
    {
        "name": "Blocco mossa vincente Umano",
        "grid": [
            [PLAYER_X, PLAYER_X, EMPTY],
            [EMPTY, PLAYER_O, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ],
        "expected": (0, 2),
    },
]


@pytest.mark.parametrize("test_case", SCENARIOS)
def test_ai_logic(test_case):
    """Testa diverse situazioni di gioco per verificare l'ottimalità dell'IA."""
    # Arrange
    board = Board()
    board.grid = test_case["grid"]
    # Act
    move = get_best_move(board)
    # Assert
    assert move == test_case["expected"], f"Fallito: {test_case['name']}"
