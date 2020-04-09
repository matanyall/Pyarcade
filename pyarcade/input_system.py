from pyarcade.games.mastermind import Mastermind
from pyarcade.games.minesweeper import Minesweeper
import re

MASTERMIND_WIDTH = 4


class InputSystem:

    def __init__(self):
        self.mastermind_game = Mastermind()
        self.minesweeper_game = Minesweeper()

    def handle_game_input(self, game_name: str, user_choice: str):
        if game_name == "Mastermind":
            return self.handle_mastermind_input(user_choice)
        elif game_name == "Minesweeper":
            return self.handle_minesweeper_input(user_choice)
        else:
            return self.invalid_input(user_choice)

    @staticmethod
    def invalid_input(invalid_input: str) -> str:
        output_msg = """
           {0} is not recognized as a game input or command.

           Type 'help' to view all game inputs and commands.
           """.format(invalid_input)
        return output_msg

    def handle_mastermind_input(self, guess_input):
        """
        Takes:
            string str that we ensure follows appropriate form
        Returns:
            hidden_sequence List[int]: A sequence of integers to be guessed by the player.
        """
        if type(guess_input) == str:
            if guess_input == "Clear Game History":
                return self.mastermind_game.clear()
            if guess_input == "Reset Game":
                return self.mastermind_game.reset()

            guess = list(guess_input)
            guess_output = []
            for idx in range(0, len(guess)):
                if guess[idx].isdigit():
                    guess_output.append(int(guess[idx]))

            if len(guess_output) != MASTERMIND_WIDTH:
                return self.invalid_input(guess_input)
            return self.mastermind_game.evaluate(guess_output)
        return self.invalid_input(guess_input)

    def handle_minesweeper_input(self, location_input: str):
        if type(location_input) == str:
            two_comma_separated_digits_regex = r"^\d,\d$"
            if re.search(two_comma_separated_digits_regex, location_input):
                location_guess = location_input.split(',')
                return self.minesweeper_game.make_move([int(location_guess[0]), int(location_guess[1])])
            elif location_input == "Reset Game":
                return self.minesweeper_game.reset_game()
            elif location_input == "Clear Game History":
                return self.minesweeper_game.clear_game_history()

        return self.invalid_input(location_input)
