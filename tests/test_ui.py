"""Modulo di test per l'interfaccia utente console."""

from pytest_mock import MockerFixture
from src.modules.ui import ConsoleUI


def test_get_player_move_valid(mocker: MockerFixture):
    """Verifica che l'input dell'utente venga convertito in coordinate (r, c)."""
    # Arrange
    ui = ConsoleUI()
    mocker.patch("builtins.input", return_value="1 1")
    spy = mocker.spy(ui, "get_player_move")

    # Act
    move = ui.get_player_move()

    # Assert
    assert move == (1, 1)
    assert spy.call_count == 1


def test_show_message_output(mocker: MockerFixture):
    """Verifica che il messaggio venga stampato con la formattazione corretta."""
    # Arrange
    ui = ConsoleUI()
    mock_print = mocker.patch("builtins.print")

    # Act
    ui.show_message("Benvenuto")

    # Assert
    mock_print.assert_called_with("*** Benvenuto ***")
