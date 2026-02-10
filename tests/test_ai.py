import unittest

from src.modules.ai import get_best_move, minimax
from src.modules.board import PLAYER_O, PLAYER_X, Board


class TestAI(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_ai_wins_immediately(self):
        self.board.grid[0][0] = PLAYER_O
        self.board.grid[0][1] = PLAYER_O
        move = get_best_move(self.board)
        self.assertEqual(move, (0, 2))

    def test_ai_blocks_player(self):
        self.board.grid[1][0] = PLAYER_X
        self.board.grid[1][1] = PLAYER_X
        move = get_best_move(self.board)
        self.assertEqual(move, (1, 2))

    def test_ai_prefers_center_on_empty_board(self):
        move = get_best_move(self.board)
        self.assertEqual(move, (1, 1))

    def test_minimax_terminal_state_win(self):
        self.board.grid[0] = [PLAYER_O, PLAYER_O, PLAYER_O]
        score = minimax(self.board, 0, False)
        self.assertEqual(score, 10)

    def test_minimax_terminal_state_loss(self):
        self.board.grid[0] = [PLAYER_X, PLAYER_X, PLAYER_X]
        score = minimax(self.board, 0, True)
        self.assertEqual(score, -10)