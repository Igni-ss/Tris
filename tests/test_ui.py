import unittest
from io import StringIO
from unittest.mock import patch

from src.modules.board import EMPTY
from src.modules.ui import ConsoleUI


class TestUI(unittest.TestCase):
    def setUp(self):
        self.ui = ConsoleUI()

    def test_display_board_output(self):
        grid = [[EMPTY, "X", EMPTY], [EMPTY, "O", EMPTY], [EMPTY, EMPTY, EMPTY]]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.ui.display_board(grid)
            output = fake_out.getvalue()
            self.assertIn("X", output)
            self.assertIn("O", output)
            self.assertIn("---+---+---", output)

    @patch('builtins.input', side_effect=['1 1'])
    def test_get_player_move_valid(self, mock_input):
        move = self.ui.get_player_move()
        self.assertEqual(move, (1, 1))

    @patch('builtins.input', side_effect=['invalid', '1,2'])
    def test_get_player_move_retry(self, mock_input):
        move = self.ui.get_player_move()
        self.assertEqual(move, (1, 2))

    def test_show_message(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.ui.show_message("Test Message")
            self.assertIn("*** Test Message ***", fake_out.getvalue())