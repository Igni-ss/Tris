"""Modulo di test per l'algoritmo Minimax dell'IA."""

import pytest  # type: ignore

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
    {
        "name": "Blocco mossa vincente Umano",
        "grid": [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ],
        "expected": (1, 1),
    },
]


@pytest.mark.parametrize("test_case", SCENARIOS)
def test_ai_logic(test_case):
    """
    Testa diverse situazioni di gioco per verificare l'ottimalità dell'IA.
    Segue il pattern Arrange-Act-Assert (AAA).
    """
    # Arrange [cite: 597, 599]
    board = Board()
    board.grid = test_case["grid"]

    # Act [cite: 597, 600]
    move = get_best_move(board)

    # Assert [cite: 597, 601]
    assert move == test_case["expected"], f"Fallito: {test_case['name']}"
