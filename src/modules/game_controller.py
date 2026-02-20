from .ai import get_best_move
from .board import PLAYER_O, PLAYER_X, Board
from .ui import GUI


class GameController:
    def __init__(self) -> None:
        self.board = Board()
        self.gui = GUI(self.on_move, self.start_new_game)
        self.current_player = PLAYER_X
        self.gui.show_message("BENVENUTO A TRIS IMBATTIBILE!")
        self.gui.mainloop()

    def start_new_game(self) -> None:
        self.board = Board()
        self.current_player = PLAYER_X
        self.gui.display_board(self.board.grid)
        self.gui.show_message("BENVENUTO A TRIS IMBATTIBILE!")

    def on_move(self, r: int, c: int):
        if self.board.check_winner() or self.board.is_full():
            return
        if self.current_player == PLAYER_X:
            if not self.board.make_move(r, c, PLAYER_X):
                self.gui.show_error("Mossa non valida o cella occupata! Riprova.")
                return
            self.gui.display_board(self.board.grid)
            winner = self.board.check_winner()
            if winner:
                self.gui.show_message(f"PARTITA FINITA! Ha vinto: {winner}")
                self.gui.show_restart(True)
                return
            if self.board.is_full():
                self.gui.show_message("PARTITA FINITA! Pareggio.")
                self.gui.show_restart(True)
                return
            self.PC_move()

    def PC_move(self) -> None:
        self.gui.show_message("Il PC sta pensando...")
        row, col = get_best_move(self.board)
        self.board.make_move(row, col, PLAYER_O)
        self.gui.display_board(self.board.grid)
        self.gui.show_message(f"Il PC ha giocato in {row} {col}")
        winner = self.board.check_winner()
        if winner:
            self.gui.show_message(f"PARTITA FINITA! Ha vinto: {winner}")
            self.gui.show_restart(True)
            return
        if self.board.is_full():
            self.gui.show_message("PARTITA FINITA! Pareggio.")
            self.gui.show_restart(True)
            return
        self.current_player = PLAYER_X
