"""
Modulo per l'interfaccia utente da console.
"""

import tkinter as tk
from typing import Any, Callable, List

from .ai import Difficulty


class GUI:
    """
    Gestisce l'interfaccia grafica del gioco, inclusi i pulsanti della scacchiera e i messaggi
    di stato.
    """

    def __init__(
        self,
        on_move: Callable[[int, int], None],
        on_restart: Callable[[], None],
        on_difficulty_change: Callable[[], None],
        difficulty: Difficulty = Difficulty.MEDIUM,
    ):
        self.root = tk.Tk()
        self.root.title("Tris")
        self.buttons: List[List[tk.Button]] = []
        self.callbacks: dict[str, Callable] = {
            "on_move": on_move,
            "on_restart": on_restart,
            "on_difficulty_change": on_difficulty_change,
        }
        self.difficulty = difficulty
        self.status_var = tk.StringVar()
        self.widgets: dict[str, Any] = {}
        self._build_grid()
        self._build_status()

    def _build_grid(self):
        """Costruisce la griglia 3x3 di pulsanti per il gioco."""
        for r in range(3):
            row = []
            for c in range(3):
                btn = tk.Button(
                    self.root,
                    text="",
                    font=("Arial", 32),
                    width=3,
                    height=1,
                    command=lambda r=r, c=c: self.callbacks["on_move"](r, c),
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

    def _build_status(self):
        """
        Costruisce l'area di visualizzazione dei messaggi di stato e il pulsante di restart.
        """
        self.widgets["status_label"] = tk.Label(
            self.root, textvariable=self.status_var, font=("Arial", 14)
        )
        self.widgets["status_label"].grid(row=3, column=0, columnspan=3, pady=10)

        self.widgets["difficulty_button"] = tk.Button(
            self.root,
            text=f"Difficoltà: {self.difficulty.name}",
            font=("Arial", 12),
            command=self._on_difficulty_click,
        )
        self.widgets["difficulty_button"].grid(row=4, column=0, columnspan=3, pady=5)
        self.widgets["restart_button"] = tk.Button(
            self.root,
            text="Ricomincia",
            font=("Arial", 14),
            command=self._on_restart_click,
        )
        self.widgets["restart_button"].grid(row=5, column=0, columnspan=3, pady=10)
        self.widgets["restart_button"].grid_remove()

    def show_restart(self, show: bool = True):
        """Mostra o nasconde il pulsante di restart."""
        btn = self.widgets.get("restart_button")
        if btn:
            if show:
                btn.grid()
            else:
                btn.grid_remove()

    def _on_restart_click(self):
        """Gestisce il click sul pulsante di restart e chiama la callback associata."""
        cb = self.callbacks.get("on_restart")
        if cb:
            cb()

    def _on_difficulty_click(self):
        """Gestisce il click sul pulsante di difficoltà e chiama la callback associata."""
        cb = self.callbacks.get("on_difficulty_change")
        if cb:
            cb()

    def display_board(self, grid: List[List[str]]) -> None:
        """Aggiorna i pulsanti della griglia per riflettere lo stato attuale del gioco."""
        for r in range(3):
            for c in range(3):
                self.buttons[r][c]["text"] = grid[r][c] if grid[r][c] else ""
        self.show_restart(False)

    def show_message(self, msg: str) -> None:
        """Visualizza un messaggio di stato all'utente."""
        self.status_var.set(msg)
        self.update_status_color("black")

    def show_error(self, err: str) -> None:
        """Visualizza un messaggio di errore all'utente."""
        self.status_var.set(f"Errore: {err}")
        self.update_status_color("red")

    def update_status_color(self, color: str) -> None:
        """Aggiorna il colore del testo del messaggio di stato."""
        label = self.widgets.get("status_label")
        if label:
            label.config(fg=color)

    def show_difficulty(self, difficulty: Difficulty) -> None:
        """Aggiorna il testo del pulsante della difficoltà."""
        btn = self.widgets.get("difficulty_button")
        if btn:
            btn.config(text=f"Difficoltà: {difficulty.name}")

    def mainloop(self):
        """Avvia il loop principale dell'interfaccia grafica."""
        self.root.mainloop()
