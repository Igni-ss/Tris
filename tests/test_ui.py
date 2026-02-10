"""Modulo di test per l'interfaccia utente console."""

from pytest_mock import MockerFixture

from src.modules.ui import ConsoleUI


def test_get_player_move_valid(mocker: MockerFixture):
    """
    Verifica che l'input dell'utente venga convertito in coordinate (r, c).
    Utilizza un Mock per simulare l'input da tastiera.
    """
    # Arrange [cite: 86, 132]
    ui = ConsoleUI()
    mocker.patch("builtins.input", return_value="1 1")
    spy = mocker.spy(ui, "get_player_move")  # [cite: 110, 139]

    # Act [cite: 89, 142]
    move = ui.get_player_move()

    # Assert [cite: 91, 147]
    assert move == (1, 1)
    assert spy.call_count == 1
