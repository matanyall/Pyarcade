import pytest
from pyarcade.input_system import InputSystem
import unittest


@pytest.mark.local
class InputSystemTestCase(unittest.TestCase):
    def test_mastermind_wrong_size(self):
        input_system = InputSystem()
        result = input_system.handle_game_input("Mastermind", "53255")
        self.assertEqual(True, "Invalid input" in result)

    def test_mastermind_clear(self):
        input_system = InputSystem()
        self.assertEqual("History cleared", input_system.handle_mastermind_input("Clear"))

    def test_mastermind_reset(self):
        input_system = InputSystem()
        result = input_system.handle_mastermind_input("reset")
        self.assertEqual(True, "Game reset" in result)

    def test_mastermind_help(self):
        input_system = InputSystem()
        result = input_system.handle_mastermind_input("help")
        self.assertEqual(True, "bulls are numbers" in result)

    def test_mastermind_invalid_input(self):
        input_system = InputSystem()
        result = input_system.handle_mastermind_input(1234)
        self.assertEqual(True, "Invalid input" in result)

    def test_valid_minesweeper_choice_invalid_input(self):
        input_sys = InputSystem()
        result = input_sys.handle_game_input("Minesweeper", "string")
        self.assertEqual(True, "Invalid input" in result)

    def test_minesweeper_input_reset(self):
        i_s = InputSystem()
        i_s.handle_minesweeper_input("4,3")
        result = i_s.handle_minesweeper_input("Reset")
        self.assertEqual(True, "Game reset" in result)

    def test_minesweeper_input_clear(self):
        in_sys = InputSystem()
        in_sys.handle_minesweeper_input("4,3")
        self.assertEqual([[4, 3]], in_sys.minesweeper_game.game_history)
        self.assertEqual([[4, 3]], in_sys.minesweeper_game.game_history)

    def test_minesweeper_input_invalid(self):
        in_sys = InputSystem()
        result = in_sys.handle_minesweeper_input("Mines")
        self.assertEqual(True, "Invalid input" in result)
        result = in_sys.handle_minesweeper_input("1,2,3")
        self.assertEqual(True, "Invalid input" in result)

    def test_minesweeper_input_help(self):
        i_s = InputSystem()
        result = i_s.handle_minesweeper_input("help")
        self.assertEqual(True, "find all the mines" in result)

    def test_handle_game_input_correct(self):
        in_sys = InputSystem()
        in_sys.handle_game_input("Minesweeper", "1,2")
        self.assertEqual([[1, 2]], in_sys.minesweeper_game.game_history)

    def test_handle_game_input_incorrect(self):
        in_sys = InputSystem()
        result = in_sys.handle_game_input("Go Fish", "1,2")
        self.assertEqual(True, "Invalid game" in result)

    def test_crazy_eights_input_invalid(self):
        input_sys = InputSystem()
        result = input_sys.handle_crazy_eights_input("345")
        self.assertEqual(True, "Invalid input" in result)

    def test_crazy_eights_input_valid(self):
        input_sys = InputSystem()
        result = input_sys.handle_crazy_eights_input("Eight,Spades")
        self.assertEqual(True, "Player Hand" in result)

    def test_crazy_eights_input_clear(self):
        input_sys = InputSystem()
        result = input_sys.handle_crazy_eights_input("clear")
        self.assertEqual(True, "History cleared" in result)

    def test_crazy_eights_game(self):
        input_sys = InputSystem()
        result = input_sys.handle_game_input("Crazy Eights", "Eight,Spades")
        self.assertEqual(True, "Player Hand" in result)

    def test_crazy_eights_input_help(self):
        input_sys = InputSystem()
        result = input_sys.handle_crazy_eights_input("help")
        self.assertEqual(True, "matches either the suit" in result)

    def test_blackjack_input_invalid(self):
        input_sys = InputSystem()
        result = input_sys.handle_blackjack_input("345")
        self.assertEqual(True, "Invalid input" in result)

    def test_blackjack_input_valid(self):
        input_sys = InputSystem()
        result = input_sys.handle_blackjack_input("hit")
        self.assertEqual(True, "CURRENT HAND" in result)

    def test_blackjack_input_help(self):
        input_sys = InputSystem()
        result = input_sys.handle_blackjack_input("help")
        self.assertEqual(True, "If your hand's sum" in result)

    def test_blackjack_input_clear(self):
        input_sys = InputSystem()
        result = input_sys.handle_blackjack_input("clear")
        self.assertEqual(True, "History cleared" in result)

    def test_blackjack_game(self):
        input_sys = InputSystem()
        result = input_sys.handle_game_input("BlackJack", "stand")
        self.assertEqual(True, "CURRENT HAND" in result)
