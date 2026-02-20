"""
Modulo per l'interfaccia utente da console.
"""

import tkinter as tk
from typing import Callable, List, Optional


class GUI:
    def __init__(
        self, on_move: Callable[[int, int], None], on_restart: Callable[[], None]
    ):
        self.root = tk.Tk()
        self.root.title("Tris")
        self.buttons: List[List[tk.Button]] = []
        self.on_move = on_move
        self.on_restart = on_restart
        self.status_var = tk.StringVar()
        self.restart_button = None
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
        self.status_label = tk.Label(
            self.root, textvariable=self.status_var, font=("Arial", 14)
        )
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10)

        self.restart_button = tk.Button(
            self.root,
            text="Ricomincia",
            font=("Arial", 14),
            command=self._on_restart_click,
        )
        self.restart_button.grid(row=4, column=0, columnspan=3, pady=10)
        self.restart_button.grid_remove()

    def show_restart(self, show: bool = True):
        if self.restart_button:
            if show:
                self.restart_button.grid()
            else:
                self.restart_button.grid_remove()

    def _on_restart_click(self):
        if self.on_restart:
            self.on_restart()

    def display_board(self, grid: List[List[str]]) -> None:
        for r in range(3):
            for c in range(3):
                self.buttons[r][c]["text"] = grid[r][c] if grid[r][c] else ""
        self.show_restart(False)

    def show_message(self, msg: str) -> None:
        self.status_var.set(msg)
        self._update_status_color("black")

    def show_error(self, err: str) -> None:
        self.status_var.set(f"Errore: {err}")
        self._update_status_color("red")

    def _update_status_color(self, color: str) -> None:
        self.status_label.config(fg=color)

    def mainloop(self):
        self.root.mainloop()
