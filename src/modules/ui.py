"""
Modulo per l'interfaccia utente da console.
"""

import tkinter as tk
from typing import Callable, List


class GUI:
    def __init__(self, on_move: Callable[[int, int], None]):
        self.root = tk.Tk()
        self.root.title("Tris")
        self.buttons: List[List[tk.Button]] = []
        self.on_move = on_move
        self.status_var = tk.StringVar()
        self._build_grid()
        self._build_status()

    def _build_grid(self):
        for r in range(3):
            row = []
            for c in range(3):
                btn = tk.Button(
                    self.root,
                    text="",
                    font=("Arial", 32),
                    width=3,
                    height=1,
                    command=lambda r=r, c=c: self.on_move(r, c),
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

    def _build_status(self):
        status_label = tk.Label(
            self.root, textvariable=self.status_var, font=("Arial", 14)
        )
        status_label.grid(row=3, column=0, columnspan=3, pady=10)

    def display_board(self, grid: List[List[str]]) -> None:
        for r in range(3):
            for c in range(3):
                self.buttons[r][c]["text"] = grid[r][c] if grid[r][c] else ""

    def show_message(self, msg: str) -> None:
        self.status_var.set(msg)

    def show_error(self, err: str) -> None:
        self.status_var.set(f"Errore: {err}")

    def mainloop(self):
        self.root.mainloop()
