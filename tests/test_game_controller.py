"""Test per il modulo GameController"""

import pytest

from src.modules.ai import Difficulty
from src.modules.board import PLAYER_O, PLAYER_X
from src.modules.game_controller import GameController
from src.modules.ui import Mode


# pylint: disable=redefined-outer-name
@pytest.fixture
def controller_and_mocks(mocker):
    """Fixture per creare un'istanza di GameController con Board, GUI e get_best_move mockati."""
    # Mock GUI e get_best_move
    mock_gui = mocker.patch("src.modules.game_controller.GUI")
    mock_get_best_move = mocker.patch("src.modules.game_controller.get_best_move")

    # Disabilita __init__ per evitare mainloop
    mocker.patch.object(GameController, "__init__", lambda self: None)
    controller = GameController()
    controller.board = mocker.MagicMock()
    controller.gui = mock_gui.return_value
    controller.current_player = PLAYER_X
    controller.difficulty = Difficulty.MEDIUM
    controller.mode = Mode.PC
    return controller, controller.board, controller.gui, mock_get_best_move


def test_init_controller(mocker):
    """
    Testa che l'inizializzazione di GameController crei correttamente Board, GUI e mostri
    il messaggio di benvenuto.
    """
    mock_gui = mocker.patch("src.modules.game_controller.GUI")
    mock_board = mocker.patch("src.modules.game_controller.Board")

    controller = GameController()

    mock_board.assert_called_once()
    mock_gui.assert_called_once()
    mock_gui().show_message.assert_called_with("BENVENUTO A TRIS GUI!")
    mock_gui().mainloop.assert_called_once()
    assert controller.current_player == PLAYER_X


def test_start_new_game(mocker, controller_and_mocks):
    """Testa che start_new_game resetti correttamente lo stato del gioco, aggiorni la scacchiera"""
    controller, _, gui, _ = controller_and_mocks
    mock_board = mocker.patch("src.modules.game_controller.Board")

    controller.start_new_game()

    assert controller.current_player == PLAYER_X
    assert isinstance(controller.board, type(mock_board.return_value))
    gui.display_board.assert_called_once_with(mock_board.return_value.grid)
    gui.show_message.assert_called_with("BENVENUTO A TRIS GUI!")


SCENARIOS_ON_MOVE = [
    {
        "name": "Mossa valida e chiama pc_move",
        "make_move": True,
        "check_game_over": False,
        "mode": Mode.PC,
        "current_player": PLAYER_X,
        "expected_calls": ["make_move", "pc_move"],
    },
    {
        "name": "Mossa valida e cambia giocatore in PvP",
        "make_move": True,
        "check_game_over": False,
        "mode": Mode.PVP,
        "current_player": PLAYER_X,
        "expected_calls": ["make_move", "change_player"],
    },
    {
        "name": "Mossa non valida",
        "make_move": False,
        "check_game_over": False,
        "mode": Mode.PC,
        "current_player": PLAYER_X,
        "expected_calls": ["invalid_move"],
    },
    {
        "name": "Game over dopo mossa valida",
        "make_move": True,
        "check_game_over": True,
        "mode": Mode.PC,
        "current_player": PLAYER_X,
        "expected_calls": ["make_move", "check_game_over"],
    },
]


@pytest.mark.parametrize("test_case", SCENARIOS_ON_MOVE)
def test_on_move_parametrized(mocker, controller_and_mocks, test_case):
    """
    Test parametrico per on_move: verifica comportamento in caso di mossa valida, partita finita,
    mossa non valida, vittoria e pareggio.
    """
    controller, board, gui, mock_get_best_move = controller_and_mocks
    controller.mode = test_case["mode"]
    controller.current_player = test_case["current_player"]

    make_move = test_case["make_move"]
    expected_calls = test_case["expected_calls"]

    if make_move is not None:
        board.make_move.return_value = make_move

    mock_check_game_over = mocker.patch.object(
        controller, "check_game_over", return_value=test_case["check_game_over"]
    )

    # Patch pc_move se serve
    if "pc_move" in expected_calls:
        mock_pc_move = mocker.patch.object(controller, "pc_move")
    else:
        mock_pc_move = None

    mock_get_best_move.return_value = (1, 1)

    controller.on_move(0, 0)

    if "make_move" in expected_calls:
        board.make_move.assert_any_call(0, 0, PLAYER_X)
    if "invalid_move" in expected_calls:
        gui.show_error.assert_called_with("Mossa non valida o cella occupata! Riprova.")
        gui.display_board.assert_not_called()
    if "check_game_over" in expected_calls:
        mock_check_game_over.assert_called_once()
    if "pc_move" in expected_calls and mock_pc_move is not None:
        mock_pc_move.assert_called_once()
    if "change_player" in expected_calls:
        assert controller.current_player == PLAYER_O
    if "no_move" in expected_calls:
        board.make_move.assert_not_called()
        gui.display_board.assert_not_called()


def test_cycle_mode(controller_and_mocks):
    """Testa che cycle_mode cicli correttamente tra le modalità di gioco e aggiorni la GUI."""
    controller, _, gui, _ = controller_and_mocks
    initial_mode = controller.mode

    controller.cycle_mode()
    assert controller.mode != initial_mode
    gui.update_mode.assert_called_with(controller.mode)
    if controller.mode == Mode.PC:
        gui.show_difficulty.assert_called_with(True)
    else:
        gui.show_difficulty.assert_called_with(False)

    controller.cycle_mode()
    assert controller.mode == initial_mode
    gui.update_mode.assert_called_with(controller.mode)
    if controller.mode == Mode.PC:
        gui.show_difficulty.assert_called_with(True)
    else:
        gui.show_difficulty.assert_called_with(False)


def test_cycle_difficulty(controller_and_mocks):
    """Testa che cycle_difficulty cicli correttamente tra le difficoltà e aggiorni il pulsante."""
    controller, _, gui, _ = controller_and_mocks
    initial_difficulty = controller.difficulty

    controller.cycle_difficulty()
    assert controller.difficulty != initial_difficulty
    gui.update_difficulty.assert_called_with(controller.difficulty)

    controller.cycle_difficulty()
    assert controller.difficulty != initial_difficulty
    gui.update_difficulty.assert_called_with(controller.difficulty)

    controller.cycle_difficulty()
    assert controller.difficulty == initial_difficulty
    gui.update_difficulty.assert_called_with(controller.difficulty)


# Scenari parametrizzati per test_pc_move
SCENARIOS_PC_MOVE = [
    {
        "name": "Mossa normale PC",
        "check_winner_return": None,
        "is_full_return": False,
        "expected_message": "Il PC ha giocato in 1 1",
    },
    {
        "name": "Vittoria PC",
        "check_winner_return": PLAYER_O,
        "is_full_return": False,
        "expected_message": "Il PC ha giocato in 1 1",
    },
    {
        "name": "Pareggio",
        "check_winner_return": None,
        "is_full_return": True,
        "expected_message": "Il PC ha giocato in 1 1",
    },
]


@pytest.mark.parametrize("scenario", SCENARIOS_PC_MOVE)
def test_pc_move_parametrized(controller_and_mocks, scenario):
    """
    Test parametrico per pc_move: verifica comportamento in caso di mossa normale, vittoria
    o pareggio.
    """
    controller, board, gui, mock_get_best_move = controller_and_mocks
    mock_get_best_move.return_value = (1, 1)
    board.make_move.return_value = True
    board.check_winner.return_value = scenario["check_winner_return"]
    board.is_full.return_value = scenario["is_full_return"]

    controller.pc_move()

    gui.show_message.assert_any_call("Il PC sta pensando...")
    mock_get_best_move.assert_called_once_with(board, controller.difficulty)
    board.make_move.assert_called_once_with(1, 1, PLAYER_O)
    gui.display_board.assert_called_once_with(board.grid)
    gui.show_message.assert_any_call(scenario["expected_message"])
    assert controller.current_player == PLAYER_X


def test_check_game_over_no_winner(controller_and_mocks):
    """
    Testa che check_game_over ritorni False se la partita non è finita (nessun vincitore e
    scacchiera non piena).
    """
    controller, board, _, _ = controller_and_mocks
    board.check_winner.return_value = None
    board.is_full.return_value = False

    result = controller.check_game_over()

    assert result is False


def test_check_game_over_winner(controller_and_mocks):
    """
    Testa che check_game_over ritorni True e mostri il messaggio di vittoria se c'è un vincitore.
    """
    controller, board, gui, _ = controller_and_mocks
    board.check_winner.return_value = PLAYER_X

    result = controller.check_game_over()

    assert result is True
    gui.show_message.assert_called_with("PARTITA FINITA! Ha vinto: X")
    gui.show_restart.assert_called_with(True)
