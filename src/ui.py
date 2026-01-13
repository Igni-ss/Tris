"""
Modulo per l'interfaccia utente da console.
"""

from typing import List, Tuple


class ConsoleUI:
    """
    Gestisce l'interazione con l'utente (Input/Output).
    Serve a tenere il main pulito e leggibile.
    """

    def display_board(self, grid: List[List[str]]) -> None:
        """Stampa la griglia di gioco."""
        print("\n")
        for i, row in enumerate(grid):
            print(f" {row[0]} | {row[1]} | {row[2]} ")
            if i < 2:
                print("---+---+---")
        print("\n")

    def get_player_move(self) -> Tuple[int, int]:
        """Chiede all'utente la mossa finché non inserisce dati validi."""
        while True:
            try:
                inp = input("Il tuo turno (X). Inserisci riga e colonna (0-2): ")
                # Gestisce input tipo "1 1" oppure "1,1"
                parts = inp.replace(",", " ").split()

                if len(parts) != 2:
                    print("Devi inserire due numeri separati da spazio.")
                    continue

                r, c = map(int, parts)
                return r, c
            except ValueError:
                print("Input non valido. Inserisci numeri interi (es: 1 1).")

    def show_message(self, msg: str) -> None:
        """Mostra un messaggio informativo all'utente."""
        print(f"*** {msg} ***")

    def show_error(self, err: str) -> None:
        """Mostra un messaggio di errore."""
        print(f"!!! {err} !!!")
