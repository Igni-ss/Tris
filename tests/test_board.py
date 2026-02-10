import unittest

from src.modules.board import EMPTY, PLAYER_O, PLAYER_X, Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_board_empty(self):
        for row in self.board.grid:
            for cell in row:
                self.assertEqual(cell, EMPTY)

    def test_make_move_valid(self):
        result = self.board.make_move(0, 0, PLAYER_X)
        self.assertTrue(result)
        self.assertEqual(self.board.grid[0][0], PLAYER_X)

    def test_make_move_invalid_occupied(self):
        self.board.make_move(1, 1, PLAYER_X)
        result = self.board.make_move(1, 1, PLAYER_O)
        self.assertFalse(result)
        self.assertEqual(self.board.grid[1][1], PLAYER_X)

    def test_make_move_out_of_bounds(self):
        self.assertFalse(self.board.make_move(3, 0, PLAYER_X))
        self.assertFalse(self.board.make_move(-1, 0, PLAYER_X))

    def test_check_winner_row(self):
        self.board.grid[0] = [PLAYER_X, PLAYER_X, PLAYER_X]
        self.assertEqual(self.board.check_winner(), PLAYER_X)

    def test_check_winner_column(self):
        for i in range(3):
            self.board.grid[i][1] = PLAYER_O
        self.assertEqual(self.board.check_winner(), PLAYER_O)

    def test_check_winner_diagonal(self):
        for i in range(3):
            self.board.grid[i][i] = PLAYER_X
        self.assertEqual(self.board.check_winner(), PLAYER_X)

    def test_is_full(self):
        self.board.grid = [[PLAYER_X, PLAYER_O, PLAYER_X],
                           [PLAYER_X, PLAYER_X, PLAYER_O],
                           [PLAYER_O, PLAYER_X, PLAYER_O]]
        self.assertTrue(self.board.is_full())

    def test_get_available_moves(self):
        self.board.grid[0][0] = PLAYER_X
        moves = self.board.get_available_moves()
        self.assertEqual(len(moves), 8)
        self.assertNotIn((0, 0), moves)