from src.modules.board import EMPTY, PLAYER_O, PLAYER_X, Board


def test_make_move_success():
    # Arrange: inizializza la scacchiera
    board = Board()
    # Act: esegue una mossa valida
    result = board.make_move(1, 1, PLAYER_X)
    # Assert: verifica lo stato
    assert result is True
    assert board.grid[1][1] == PLAYER_X


def test_make_move_invalid_occupied():
    # Arrange
    board = Board()
    board.make_move(0, 0, PLAYER_X)
    # Act
    result = board.make_move(0, 0, PLAYER_O)
    # Assert
    assert result is False


def test_check_winner_horizontal():
    # Arrange
    board = Board()
    board.grid[0] = [PLAYER_X, PLAYER_X, PLAYER_X]
    # Act & Assert
    assert board.check_winner() == PLAYER_X


def test_is_full_true():
    # Arrange
    board = Board()
    board.grid = [[PLAYER_X, PLAYER_O, PLAYER_X] for _ in range(3)]
    # Act & Assert
    assert board.is_full() is True
