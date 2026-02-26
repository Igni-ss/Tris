"""Modulo di test per l'algoritmo Minimax dell'IA."""

import pytest  # type: ignore
from pytest_mock import MockerFixture  # type: ignore

from src.modules.ai import Difficulty, get_best_move
from src.modules.board import EMPTY, PLAYER_O, PLAYER_X, Board

SCENARIOS_HARD = [
    {
        "name": "Vittoria immediata PC in HARD",
        "grid": [
            [PLAYER_O, PLAYER_O, EMPTY],
            [EMPTY, PLAYER_X, EMPTY],
            [EMPTY, EMPTY, PLAYER_X],
        ],
        "difficulty": Difficulty.HARD,
        "expected": (0, 2),
    },
    {
        "name": "Blocco mossa vincente Umano in HARD",
        "grid": [
            [PLAYER_X, PLAYER_X, EMPTY],
            [EMPTY, PLAYER_O, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ],
        "difficulty": Difficulty.HARD,
        "expected": (0, 2),
    },
    {
        "name": "Blocco mossa vincente Umano in HARD",
        "grid": [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ],
        "difficulty": Difficulty.HARD,
        "expected": (1, 1),
    },
]


@pytest.mark.parametrize("test_case", SCENARIOS_HARD)
def test_ai_logic_hard(test_case):
    """
    Testa diverse situazioni di gioco per verificare l'ottimalità dell'IA.
    Segue il pattern Arrange-Act-Assert (AAA).
    """
    # Arrange [cite: 597, 599]
    board = Board()
    board.grid = test_case["grid"]

    # Act [cite: 597, 600]
    move = get_best_move(board, difficulty=test_case["difficulty"])

    # Assert [cite: 597, 601]
    assert move == test_case["expected"], f"Fallito: {test_case['name']}"


def test_ai_easy():
    """
    Testa che in modalità EASY l'IA restituisca una mossa valida ma non necessariamente
    ottimale.
    """
    board = Board()
    board.grid = [
        [PLAYER_O, PLAYER_O, EMPTY],
        [EMPTY, PLAYER_X, EMPTY],
        [EMPTY, EMPTY, PLAYER_X],
    ]
    move = get_best_move(board, difficulty=Difficulty.EASY)
    assert (
        move in board.get_available_moves()
    ), f"Fallito: EASY mode returned an invalid move: {move}"


def test_ai_medium_random_or_best(mocker: MockerFixture):
    """
    Testa che in modalità MEDIUM l'IA a volte restituisca una mossa casuale e a volte la mossa
    migliore, a seconda del valore restituito da random.random().
    """
    board = Board()
    board.grid = [
        [PLAYER_X, PLAYER_X, EMPTY],
        [EMPTY, PLAYER_O, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]
    mocker.patch("src.modules.ai.random.random", return_value=0.4)
    move = get_best_move(board, difficulty=Difficulty.MEDIUM)
    assert (
        move in board.get_available_moves()
    ), f"Fallito: MEDIUM mode (random) returned an invalid move: {move}"

    mocker.patch("src.modules.ai.random.random", return_value=0.6)
    move = get_best_move(board, difficulty=Difficulty.MEDIUM)
    assert move == (
        0,
        2,
    ), f"Fallito: MEDIUM mode (minimax) did not return the best move: {move}"
