import pytest

from src.modules.ui import GUI


@pytest.fixture
def gui(mocker):
    on_move = mocker.Mock()
    on_restart = mocker.Mock()
    gui = GUI(on_move, on_restart)
    yield gui
    gui.root.destroy()  # chiude la finestra dopo il test


def test_button_callback(gui):
    gui.buttons[0][1].invoke()
    gui.on_move.assert_called_once_with(0, 1)


def test_display_board(gui):
    grid = [["X", "", "O"], ["", "O", ""], ["X", "", ""]]
    gui.display_board(grid)
    assert gui.buttons[0][0]["text"] == "X"
    assert gui.buttons[0][2]["text"] == "O"
    assert gui.buttons[1][1]["text"] == "O"
    assert gui.buttons[2][0]["text"] == "X"


def test_show_message(gui):
    gui.show_message("Turno X")
    assert gui.status_var.get() == "Turno X"
    assert gui.status_label.cget("fg") == "black"


def test_show_error(gui):
    gui.show_error("Mossa non valida")
    assert gui.status_var.get() == "Errore: Mossa non valida"
    assert gui.status_label.cget("fg") == "red"


def test_status_color(gui):
    gui._update_status_color("blue")
    assert gui.status_label.cget("fg") == "blue"


def test_restart_button_callback(gui):
    gui.show_restart(True)
    gui.restart_button.invoke()
    gui.on_restart.assert_called_once()
