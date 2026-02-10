import pytest  # type: ignore
from src.modules.ai import get_best_move
from src.modules.board import EMPTY, PLAYER_O, PLAYER_X, Board

# Definizione scenari di test (GIVEN/WHEN/THEN) [cite: 685, 687, 688, 691]
scenarios = [
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


@pytest.mark.parametrize("test_case", scenarios)
def test_ai_logic(test_case):
    # Arrange
    board = Board()
    board.grid = test_case["grid"]
    # Act
    move = get_best_move(board)
    # Assert
    assert move == test_case["expected"], f"Fallito: {test_case['name']}"
