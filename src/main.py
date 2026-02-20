"""Punto di ingresso (Entry point) dell'applicazione Tris."""

import sys

from .modules.game_controller import GameController


def main():
    GameController()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPartita interrotta dall'utente.")
        sys.exit(0)
