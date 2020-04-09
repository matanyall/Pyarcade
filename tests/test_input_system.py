from pyarcade.input_system import InputSystem
import unittest


CLEAR = -1
RESET = -2
MALFORMED = -3


class InputSystemTestCase(unittest.TestCase):
    def test_success(self):
        input_system = InputSystem()
        self.assertEqual(len(input_system.handle_mastermind_input("5325")), 3)

    def test_int_list_wrong_size(self):
        input_system = InputSystem()
        result = input_system.handle_game_input("Mastermind", "53255")
        self.assertEqual(True, "not recognized as a game input or command" in result)

    def test_mastermind_clear(self):
        input_system = InputSystem()
        self.assertEqual("History cleared", input_system.handle_mastermind_input("Clear Game History"))

    def test_mastermind_reset(self):
        input_system = InputSystem()
        self.assertEqual("Game reset", input_system.handle_mastermind_input("Reset Game"))

    def test_mastermind_invalid_input(self):
        input_system = InputSystem()
        result = input_system.handle_mastermind_input(1234)
        self.assertEqual(True, "not recognized as a game input or command" in result)

    def test_valid_minesweeper_choice_invalid_input(self):
        input_sys = InputSystem()
        result = input_sys.handle_game_input("Minesweeper", "string")
        self.assertEqual(True, "not recognized as a game input or command" in result)

    def test_minesweeper_input_reset(self):
        i_s = InputSystem()
        i_s.handle_minesweeper_input("4,3")
        self.assertEqual("Game reset", i_s.handle_minesweeper_input("Reset Game"))

    def test_minesweeper_input_clear(self):
        in_sys = InputSystem()
        in_sys.handle_minesweeper_input("4,3")
        self.assertEqual([[4, 3]], in_sys.minesweeper_game.game_history)
        self.assertEqual([[4, 3]], in_sys.minesweeper_game.game_history)

    def test_minesweeper_input_invalid(self):
        in_sys = InputSystem()
        result = in_sys.handle_minesweeper_input("Mines")
        self.assertEqual(True, "not recognized as a game input or command" in result)
        result = in_sys.handle_minesweeper_input("1,2,3")
        self.assertEqual(True, "not recognized as a game input or command" in result)

    def test_handle_game_input_correct(self):
        in_sys = InputSystem()
        in_sys.handle_game_input("Minesweeper", "1,2")
        self.assertEqual([[1, 2]], in_sys.minesweeper_game.game_history)

    def test_handle_game_input_incorrect(self):
        in_sys = InputSystem()
        result = in_sys.handle_game_input("Go Fish", "1,2")
        self.assertEqual(True, "not recognized as a game input or command" in result)
