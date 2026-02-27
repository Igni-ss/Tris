"""Test per il modulo UI, che gestisce l'interfaccia grafica del gioco."""

import pytest

from src.modules.ui import GUI, GUICallbacksDict, Mode


# pylint: disable=redefined-outer-name
@pytest.fixture
def gui(mocker):
    """
    Fixture per creare un'istanza di GUI con metodi on_move e on_restart mockati
    """
    on_move = mocker.Mock()
    on_restart = mocker.Mock()
    on_difficulty_change = mocker.Mock()
    on_mode_change = mocker.Mock()
    callbacks: GUICallbacksDict = {
        "on_move": on_move,
        "on_restart": on_restart,
        "on_difficulty_change": on_difficulty_change,
        "on_mode_change": on_mode_change,
    }
    gui = GUI(callbacks)
    yield gui
    gui.root.destroy()  # chiude la finestra dopo il test


def test_button_callback(gui):
    """
    Testa che il callback on_move venga chiamato correttamente quando si clicca su un pulsante
    della griglia
    """
    gui.buttons[0][1].invoke()
    gui.callbacks["on_move"].assert_called_once_with(0, 1)


def test_difficulty_button_callback(gui):
    """
    Testa che il callback on_difficulty_change venga chiamato correttamente quando si clicca sul
    pulsante della difficoltà
    """
    gui.widgets["difficulty_button"].invoke()
    gui.callbacks["on_difficulty_change"].assert_called_once()


def test_mode_button_callback(gui):
    """
    Testa che il callback on_mode_change venga chiamato correttamente quando si clicca sul
    pulsante della modalità
    """
    gui.widgets["mode_button"].invoke()
    gui.callbacks["on_mode_change"].assert_called_once()


def test_display_board(gui):
    """
    Testa che la funzione display_board aggiorni correttamente i testi dei pulsanti in base alla
    griglia fornita
    """
    grid = [["X", "", "O"], ["", "O", ""], ["X", "", ""]]
    gui.display_board(grid)
    assert gui.buttons[0][0]["text"] == "X"
    assert gui.buttons[0][2]["text"] == "O"
    assert gui.buttons[1][1]["text"] == "O"
    assert gui.buttons[2][0]["text"] == "X"


def test_show_message(gui):
    """
    Testa che la funzione show_message aggiorni correttamente il messaggio di stato e il colore
    del testo
    """
    gui.show_message("Turno X")
    assert gui.status_var.get() == "Turno X"
    assert gui.widgets["status_label"].cget("fg") == "black"


def test_show_error(gui):
    """
    Testa che la funzione show_error aggiorni correttamente il messaggio di errore e il colore
    del testo.
    """
    gui.show_error("Mossa non valida")
    assert gui.status_var.get() == "Errore: Mossa non valida"
    assert gui.widgets["status_label"].cget("fg") == "red"


def test_status_color(gui):
    """
    Testa che la funzione update_status_color aggiorni correttamente il colore del testo del
    messaggio di stato.
    """
    gui.update_status_color("blue")
    assert gui.widgets["status_label"].cget("fg") == "blue"


def test_show_difficulty(gui):
    """
    Testa che la funzione show_difficulty mostri o nasconda correttamente il pulsante della
    difficoltà.
    """
    gui.show_difficulty(True)
    gui.root.update_idletasks()
    assert gui.widgets["difficulty_button"].winfo_ismapped() == 1
    gui.show_difficulty(False)
    gui.root.update_idletasks()
    assert gui.widgets["difficulty_button"].winfo_ismapped() == 0


def test_update_difficulty(gui):
    """
    Testa che la funzione update_difficulty aggiorni correttamente il testo del pulsante della
    difficoltà.
    """
    gui.update_difficulty(gui.difficulty)
    assert (
        gui.widgets["difficulty_button"].cget("text")
        == f"Difficoltà: {gui.difficulty.name}"
    )


def test_update_mode(gui):
    """
    Testa che la funzione update_mode aggiorni correttamente il testo del pulsante della modalità.
    """
    gui.update_mode(Mode.PVP)
    assert gui.widgets["mode_button"].cget("text") == f"Modalità: {Mode.PVP.value}"
    gui.update_mode(Mode.PC)
    assert gui.widgets["mode_button"].cget("text") == f"Modalità: {Mode.PC.value}"


def test_restart_button_callback(gui):
    """
    Testa che il callback on_restart venga chiamato correttamente quando si clicca sul pulsante
    di restart.
    """
    gui.show_restart(True)
    gui.widgets["restart_button"].invoke()
    gui.callbacks["on_restart"].assert_called_once()
