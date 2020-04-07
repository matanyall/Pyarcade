import unittest

from pyarcade.minesweeper import Minesweeper


class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_hidden_grid(self):
        self.game = Minesweeper()
        self.game.set_hidden_grid({1: [1, 2, 6], 3: [3], 4: [7], 5: [1, 5], 6: [2], 7: [1, 7]})
        self.game.draw_board()
        self.assertEqual([['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '*', '*', '-', '-', '-', '*', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '*', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '*', '-'],
                          ['-', '*', '-', '-', '-', '*', '-', '-', '-'],
                          ['-', '-', '*', '-', '-', '-', '-', '-', '-'],
                          ['-', '*', '-', '-', '-', '-', '-', '*', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-', '-']],
                         self.game.grid)

    def test_make_move_out_of_bounds(self):
        self.game = Minesweeper()
        self.game.set_hidden_grid({1: [1, 2, 6], 3: [3], 4: [7], 5: [1, 5], 6: [2], 7: [1, 7]})
        with self.assertRaises(IndexError):
            self.game.make_move([10, 2])

    def test_make_move_already_uncovered(self):
        self.game = Minesweeper()
        self.game.set_hidden_grid({1: [1, 2, 6], 3: [3], 4: [7], 5: [1, 5], 6: [2], 7: [1, 7]})
        self.game.make_move([3, 1])
        result = self.game.make_move([3, 1])
        self.assertEqual(True, "Location already uncovered" in result)

    def test_make_move_bomb(self):
        self.game = Minesweeper()
        self.game.set_hidden_grid({1: [1, 2, 6], 3: [3], 4: [7], 5: [1, 5], 6: [2], 7: [1, 7]})
        result = self.game.make_move([1, 1])
        self.assertEqual(True, "BOOM! Game over." in result)

    def test_reset(self):
        self.game = Minesweeper()
        self.game.set_hidden_grid({1: [1, 2, 6], 3: [3], 4: [7], 5: [1, 5], 6: [2], 7: [1, 7]})
        self.game.make_move([3, 1])
        self.game.reset_game()
        self.assertEqual("New game.", self.game.game_state)

    def test_clear_game_history(self):
        self.game = Minesweeper()
        self.game.set_hidden_grid({1: [1, 2, 6], 3: [3], 4: [7], 5: [1, 5], 6: [2], 7: [1, 7]})
        self.game.make_move([3, 1])
        self.game.make_move([4, 6])
        self.assertEqual([[3, 1], [4, 6]], self.game.game_history)
        self.game.clear_game_history()
        self.assertEqual([], self.game.game_history)
