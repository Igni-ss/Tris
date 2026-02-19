"""Punto di ingresso (Entry point) dell'applicazione Tris."""

import sys

from .modules.ai import get_best_move
from .modules.board import PLAYER_O, PLAYER_X, Board
from .modules.ui import GUI


def main():
    game = Board()
    current_player = PLAYER_X

    def on_move(r, c):
        nonlocal current_player
        if game.check_winner() or game.is_full():
            return
        if current_player == PLAYER_X:
            if not game.make_move(r, c, PLAYER_X):
                gui.show_error("Mossa non valida o cella occupata! Riprova.")
                return
            gui.display_board(game.grid)
            winner = game.check_winner()
            if winner:
                gui.show_message(f"PARTITA FINITA! Ha vinto: {winner}")
                return
            if game.is_full():
                gui.show_message("PARTITA FINITA! Pareggio.")
                return
            # Turno PC
            gui.show_message("Il PC sta pensando...")
            row, col = get_best_move(game)
            game.make_move(row, col, PLAYER_O)
            gui.display_board(game.grid)
            gui.show_message(f"Il PC ha giocato in {row} {col}")
            winner = game.check_winner()
            if winner:
                gui.show_message(f"PARTITA FINITA! Ha vinto: {winner}")
                return
            if game.is_full():
                gui.show_message("PARTITA FINITA! Pareggio.")
                return
            current_player = PLAYER_X

    gui = GUI(on_move)
    gui.show_message("BENVENUTO A TRIS IMBATTIBILE!")
    gui.display_board(game.grid)
    gui.mainloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPartita interrotta dall'utente.")
        sys.exit(0)
