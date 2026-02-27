"""
Il modulo GameController coordina la logica del gioco, gestisce le interazioni tra la scacchiera
e l'interfaccia utente e implementa la logica di gioco contro il PC.
"""

from .ai import Difficulty, get_best_move
from .board import PLAYER_O, PLAYER_X, Board
from .ui import GUI, GUICallbacksDict, Mode


class GameController:
    """
    Coordina la logica del gioco, gestisce le interazioni tra la scacchiera e l'interfaccia utente
    e implementa la logica di gioco contro il PC o in modalità PvP.
    """

    def __init__(self) -> None:
        self.difficulty = Difficulty.MEDIUM
        self.mode = Mode.PC
        self.board = Board()
        callbacks: GUICallbacksDict = {
            "on_move": self.on_move,
            "on_restart": self.start_new_game,
            "on_difficulty_change": self.cycle_difficulty,
            "on_mode_change": self.cycle_mode,
        }
        self.gui = GUI(
            callbacks,
            self.difficulty,
            self.mode,
        )
        self.current_player = PLAYER_X
        self.gui.show_message("BENVENUTO A TRIS GUI!")
        self.gui.mainloop()

    def start_new_game(self) -> None:
        """
        Inizializza una nuova partita, resettando la scacchiera e aggiornando l'interfaccia utente
        """
        self.board = Board()
        self.current_player = PLAYER_X
        self.gui.display_board(self.board.grid)
        self.gui.show_message("BENVENUTO A TRIS GUI!")

    def on_move(self, r: int, c: int):
        """
        Gestisce la mossa del giocatore, aggiorna la scacchiera e verifica le condizioni di vittoria
        o pareggio
        """
        if self.board.check_winner() or self.board.is_full():
            return
        if not self.board.make_move(r, c, self.current_player):
            self.gui.show_error("Mossa non valida o cella occupata! Riprova.")
            return
        self.gui.display_board(self.board.grid)
        if self.check_game_over():
            return
        if self.mode == Mode.PC:
            if self.current_player == PLAYER_X:
                self.pc_move()
        else:  # PvP
            self.current_player = (
                PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
            )

    def cycle_mode(self):
        """Cicla tra le modalità di gioco (PC/PvP) e aggiorna la GUI."""
        self.mode = Mode.PVP if self.mode == Mode.PC else Mode.PC
        self.gui.update_mode(self.mode)
        if self.mode == Mode.PC:
            self.gui.show_difficulty(True)
        else:
            self.gui.show_difficulty(False)
        self.start_new_game()

    def cycle_difficulty(self):
        """Cicla tra le difficoltà e aggiorna il pulsante e la callback."""
        difficulties = list(Difficulty)
        current_idx = difficulties.index(self.difficulty)
        next_idx = (current_idx + 1) % len(difficulties)
        self.difficulty = difficulties[next_idx]
        self.gui.update_difficulty(self.difficulty)

    def pc_move(self) -> None:
        """
        Esegue la mossa del PC, aggiorna la scacchiera e verifica le condizioni di vittoria
        o pareggio
        """
        self.gui.show_message("Il PC sta pensando...")
        row, col = get_best_move(self.board, self.difficulty)
        self.board.make_move(row, col, PLAYER_O)
        self.gui.display_board(self.board.grid)
        self.gui.show_message(f"Il PC ha giocato in {row} {col}")
        if self.check_game_over():
            return
        self.current_player = PLAYER_X

    def check_game_over(self) -> bool:
        """
        Verifica se la partita è finita, controllando se c'è un vincitore o se la scacchiera è piena
        """
        winner = self.board.check_winner()
        if winner:
            self.gui.show_message(f"PARTITA FINITA! Ha vinto: {winner}")
            self.gui.show_restart(True)
            return True
        if self.board.is_full():
            self.gui.show_message("PARTITA FINITA! Pareggio.")
            self.gui.show_restart(True)
            return True
        return False
