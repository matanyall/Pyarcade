import unittest

import pytest
from pyarcade.games.minesweeper import Minesweeper


@pytest.mark.local
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
                         self.game.hidden_grid)

    def test_make_move(self):
        self.game = Minesweeper(5, 5, 5)
        self.game.set_hidden_grid({0: [0, 2, 4], 3: [0], 4: [1]})
        self.game.make_move([3, 1])
        self.game.draw_board()
        self.assertEqual([['*', '-', '*', '-', '*'],    # 0
                          ['-', '2', '1', '2', '1'],    # 1
                          ['1', '1', ' ', ' ', ' '],    # 2
                          ['*', '2', '1', ' ', ' '],    # 3
                          ['2', '*', '1', ' ', ' ']],  # 4
                         self.game.hidden_grid)

    def test_threebv(self):
        self.game = Minesweeper(5, 5, 5)
        self.game.set_hidden_grid({0: [0, 2, 4], 3: [0], 4: [1]})
        self.game.count_threebv()
        self.assertEqual(6, self.game.get_threebv())

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

    def test_win_game(self):
        self.game = Minesweeper(5, 5, 5)
        self.game.set_hidden_grid({0: [0, 4], 1: [2], 3: [0], 4: [1]})
        result = ""
        for row_idx in range(len(self.game.hidden_grid)):
            for col_idx in range(len(self.game.hidden_grid[row_idx])):
                val = self.game.hidden_grid[row_idx][col_idx]
                if val == '-':
                    result = self.game.make_move([row_idx, col_idx])

        self.assertEqual(True, "Congratulations! You win!" in result)

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
