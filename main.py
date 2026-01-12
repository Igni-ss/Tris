import sys
from src.board import Board, PLAYER_X, PLAYER_O
from src.ai import get_best_move
from src.ui import ConsoleUI

def main():
    """
    Funzione principale che avvia il ciclo di gioco.
    """
    game = Board()
    ui = ConsoleUI()
    
    ui.show_message("BENVENUTO A TRIS IMBATTIBILE")
    ui.show_message("Tu sei la X, il PC è la O")
    
    current_player = PLAYER_X # Inizia l'umano
    
    while True:
        ui.display_board(game.grid)
        

        winner = game.check_winner()
        if winner:
            ui.show_message(f"PARTITA FINITA! Ha vinto: {winner}")
            break
        
        if game.is_full():
            ui.show_message("PARTITA FINITA! Pareggio.")
            break

        if current_player == PLAYER_X:
            row, col = ui.get_player_move()
            
            if not game.make_move(row, col, PLAYER_X):
                ui.show_error("Mossa non valida o cella occupata! Riprova.")
                continue # Salta il cambio turno, tocca ancora all'umano
                
        else:

            ui.show_message("Il PC sta pensando...")
            row, col = get_best_move(game)
            game.make_move(row, col, PLAYER_O)
            ui.show_message(f"Il PC ha giocato in {row} {col}")

        current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X
    
    ui.display_board(game.grid)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPartita interrotta dall'utente.")
        sys.exit(0)