from typing import List, Optional, Tuple

Board = List[List[str]]

PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "


class Board:
    """
    Gestisce lo stato della scacchiera, validazione delle mosse e il controllo delle condizioni
    di vittoria.
    """

    def __init__(self):
        self.grid: List[List[str]] = [[EMPTY for _ in range(3)] for _ in range(3)]

    def make_move(self, row: int, col: int, player: str) -> bool:
        """
        Tenta di eseguire una mosssa per il giocatore specificato nella posizione data

        Args:
            row (int): La riga della scacchiera (0-2).
            col (int): La colonna della scacchiera (0-2).
            player (str): Il simbolo del giocatore ("X" o "O").
        """
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        if self.grid[row][col] != EMPTY:
            return False
        self.grid[row][col] = player
        return True

    def check_winner(self) -> Optional[str]:
        """
        Verifica se c'è un vincitore sulla scacchiera.
        Returns:
            str: Il simbolo del giocatore vincente ('X' o 'O') se presente.
            None: Se non c'è un vincitore.
        """
        # Controllo righe
        for row in self.grid:
            if row[0] == row[1] == row[2] != EMPTY:
                return row[0]
        # Controllo colonne
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != EMPTY:
                return self.grid[0][col]
        # Controllo diagonali
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != EMPTY:
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != EMPTY:
            return self.grid[0][2]
        return None

    def is_full(self) -> bool:
        """Controlla se la cella è piena (Pareggio)."""
        return all(cell != EMPTY for row in self.grid for cell in row)

    def get_available_moves(self) -> List[Tuple[int, int]]:
        """Restituisce una lista di tutte le coordinate (riga,col) libere."""
        moves = []
        for r in range(3):
            for c in range(3):
                if self.grid[r][c] == EMPTY:
                    moves.append((r, c))

        return moves
