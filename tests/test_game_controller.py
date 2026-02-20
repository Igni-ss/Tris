"""Test per il modulo GameController"""

import pytest

from src.modules.board import PLAYER_O, PLAYER_X
from src.modules.game_controller import GameController


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
    mock_gui().show_message.assert_called_with("BENVENUTO A TRIS IMBATTIBILE!")
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
    gui.show_message.assert_called_with("BENVENUTO A TRIS IMBATTIBILE!")


def test_on_move_valid_and_pc_move(mocker, controller_and_mocks):
    """Testa che on_move gestisca correttamente una mossa valida del giocatore e chiami pc_move."""
    controller, board, _, mock_get_best_move = controller_and_mocks
    mock_get_best_move.return_value = (1, 1)
    mock_pc_move = mocker.patch.object(controller, "pc_move")
    board.check_winner.return_value = None
    board.is_full.return_value = False
    board.make_move.return_value = True

    controller.on_move(0, 0)

    board.make_move.assert_any_call(0, 0, PLAYER_X)
    mock_pc_move.assert_called_once()


def test_on_move_game_already_finished(controller_and_mocks):
    """Testa che on_move non permetta di fare mosse se la partita è già finita."""
    controller, board, gui, _ = controller_and_mocks
    board.check_winner.return_value = PLAYER_X
    board.is_full.return_value = False
    controller.on_move(0, 0)
    board.make_move.assert_not_called()
    gui.display_board.assert_not_called()


def test_on_move_invalid_move(controller_and_mocks):
    """
    Testa che on_move gestisca correttamente una mossa non valida (cella occupata) mostrando un
    messaggio di errore.
    """
    controller, board, gui, _ = controller_and_mocks
    board.check_winner.return_value = None
    board.is_full.return_value = False
    board.make_move.return_value = False
    controller.on_move(0, 0)
    gui.show_error.assert_called_with("Mossa non valida o cella occupata! Riprova.")
    gui.display_board.assert_not_called()


def test_on_move_player_wins(controller_and_mocks):
    """
    Testa che on_move gestisca correttamente la vittoria del giocatore mostrando il messaggio di
    vittoria e il pulsante di ricominciare.
    """
    controller, board, gui, _ = controller_and_mocks
    board.check_winner.side_effect = [None, PLAYER_X]
    board.is_full.return_value = False
    board.make_move.return_value = True
    controller.on_move(0, 0)
    gui.show_message.assert_any_call("PARTITA FINITA! Ha vinto: X")
    gui.show_restart.assert_called_with(True)


def test_on_move_draw(controller_and_mocks):
    """
    Testa che on_move gestisca correttamente la situazione di pareggio mostrando il messaggio di
    pareggio e il pulsante di ricominciare.
    """
    controller, board, gui, _ = controller_and_mocks
    board.check_winner.side_effect = [None, None]
    board.is_full.side_effect = [False, True]
    board.make_move.return_value = True
    controller.on_move(0, 0)
    gui.show_message.assert_any_call("PARTITA FINITA! Pareggio.")
    gui.show_restart.assert_called_with(True)


def test_pc_move(controller_and_mocks):
    """
    Testa che pc_move esegua correttamente la mossa del PC, aggiorni la scacchiera e mostri i
    messaggi corretti.
    """
    controller, board, gui, mock_get_best_move = controller_and_mocks
    mock_get_best_move.return_value = (1, 1)
    board.check_winner.side_effect = [None]
    board.is_full.side_effect = [False, False]
    board.make_move.return_value = PLAYER_O

    controller.pc_move()

    gui.show_message.assert_any_call("Il PC sta pensando...")
    mock_get_best_move.assert_called_once_with(board)
    board.make_move.assert_called_once_with(1, 1, PLAYER_O)
    gui.display_board.assert_called_once_with(board.grid)
    gui.show_message.assert_any_call("Il PC ha giocato in 1 1")
    board.check_winner.assert_called()
    assert controller.current_player == PLAYER_X


def test_pc_move_win(controller_and_mocks):
    """
    Testa che pc_move gestisca correttamente la vittoria del PC mostrando il messaggio di vittoria
    """
    controller, board, gui, mock_get_best_move = controller_and_mocks
    mock_get_best_move.return_value = (1, 1)
    board.check_winner.side_effect = [PLAYER_O]
    board.is_full.side_effect = [False, False]
    board.make_move.return_value = PLAYER_O

    controller.pc_move()

    mock_get_best_move.assert_called_once_with(board)
    board.make_move.assert_called_once_with(1, 1, PLAYER_O)
    gui.display_board.assert_called_once_with(board.grid)
    gui.show_message.assert_any_call("Il PC ha giocato in 1 1")
    gui.show_message.assert_any_call("PARTITA FINITA! Ha vinto: O")
    gui.show_restart.assert_called_with(True)
    board.check_winner.assert_called()
    assert controller.current_player == PLAYER_X


def test_pc_move_full(controller_and_mocks):
    """
    Testa che pc_move gestisca correttamente la situazione di pareggio mostrando il messaggio di
    pareggio.
    """
    controller, board, gui, mock_get_best_move = controller_and_mocks
    mock_get_best_move.return_value = (1, 1)
    board.check_winner.side_effect = [False]
    board.is_full.side_effect = [True]
    board.make_move.return_value = PLAYER_O

    controller.pc_move()

    mock_get_best_move.assert_called_once_with(board)
    board.make_move.assert_called_once_with(1, 1, PLAYER_O)
    gui.display_board.assert_called_once_with(board.grid)
    gui.show_message.assert_any_call("Il PC ha giocato in 1 1")
    gui.show_message.assert_any_call("PARTITA FINITA! Pareggio.")
    gui.show_restart.assert_called_with(True)
    board.check_winner.assert_called()
    assert controller.current_player == PLAYER_X
