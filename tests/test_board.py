"""
Modulo di test per la classe Board.

Controlla la logica di inserimento mosse, vittoria e riempimento scacchiera.
"""

from src.modules.board import PLAYER_O, PLAYER_X, Board


def test_make_move_success():
    """
    Testa se una mossa valida viene registrata correttamente sulla griglia.

    Segue il pattern Arrange-Act-Assert (AAA).
    """
    # Arrange
    board = Board()
    # Act
    result = board.make_move(1, 1, PLAYER_X)
    # Assert
    assert result is True
    assert board.grid[1][1] == PLAYER_X


def test_make_move_invalid_occupied():
    """
    Testa che il sistema impedisca di giocare in una cella già occupata.
    """
    # Arrange
    board = Board()
    board.make_move(0, 0, PLAYER_X)
    # Act
    result = board.make_move(0, 0, PLAYER_O)
    # Assert
    assert result is False


def test_check_winner_horizontal():
    """
    Verifica che il metodo check_winner identifichi correttamente una riga completa.
    """
    # Arrange
    board = Board()
    board.grid[0] = [PLAYER_X, PLAYER_X, PLAYER_X]
    # Act & Assert
    assert board.check_winner() == PLAYER_X


def test_is_full_true():
    """
    Verifica che la scacchiera venga identificata correttamente come piena.
    """
    # Arrange
    board = Board()
    board.grid = [[PLAYER_X, PLAYER_O, PLAYER_X] for _ in range(3)]
    # Act & Assert
    assert board.is_full() is True
