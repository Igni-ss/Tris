from pytest_mock import MockerFixture
from src.modules.ui import ConsoleUI


def test_get_player_move_valid(mocker: MockerFixture):
    # Arrange
    ui = ConsoleUI()
    # Mock dell'input utente (Slide 8)
    mock_input = mocker.patch('builtins.input', return_value="1 1")
    # Spy per verificare l'esecuzione (Slide 9)
    spy_ui = mocker.spy(ui, "get_player_move")
    
    # Act
    move = ui.get_player_move()
    
    # Assert
    assert move == (1, 1)
    assert mock_input.called

def test_show_message_output(mocker: MockerFixture):
    # Arrange
    ui = ConsoleUI()
    mock_print = mocker.patch('builtins.print')
    
    # Act
    ui.show_message("Benvenuto")
    
    # Assert
    mock_print.assert_called_with("*** Benvenuto ***")