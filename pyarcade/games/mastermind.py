from typing import Optional, List, Dict, Any
import random

total_history: Dict[int, Dict[tuple, int]] = {}
total_games = 0


class Mastermind:
    """ A class representing a Mastermind game session

        Args:
            width (int): The number of random digits to generate

            max_range (int): The range that a single digit can vary

    """

    def __init__(self, width: Optional[int] = 4, max_range: Optional[int] = 9):
        self.game_state = "New game."
        self.width = width
        self.max_range = max_range
        self.hidden_sequence = self.generate_hidden_sequence()
        self.current_history = {}
        global total_games
        total_games += 1

    def generate_hidden_sequence(self) -> List[int]:
        """
        Returns:
            hidden_sequence List[int]: A sequence of integers to be guessed by the player.
        """
        return [random.randint(0, self.max_range) for _ in range(self.width)]

    def set_hidden_sequence(self, sequence: List[int]):
        self.hidden_sequence = sequence

    def evaluate(self, user_guess: List[int]) -> str:
        """

        Args:
            user_guess:

        Returns:
            1 if digit is in the hidden sequence at the location it was submitted
            0 if digit is somewhere in the hidden sequence, but not in the location it was submitted
            -1 if the digit is nowhere in the hidden sequence
        """
        # Dictionary containing the user's guess and its evaluation
        evaluation = {}
        exact_match = True
        cows = 0
        bulls = 0

        for idx in range(len(user_guess)):
            guess = user_guess[idx]
            if guess == self.hidden_sequence[idx]:
                eval_digit = 1
                bulls += 1
            elif guess in self.hidden_sequence:
                eval_digit = 0
                exact_match = False
                cows += 1
            else:
                eval_digit = -1
                exact_match = False

            if guess not in evaluation:
                evaluation[guess] = [eval_digit]
            else:
                evaluation[guess].append(eval_digit)

        self.current_history[tuple(user_guess)] = evaluation

        if exact_match:
            str(user_guess) + ": " + str(bulls) + " bulls and " + str(cows) + " cows"
            self.game_state = "Game over."
            total_history[total_games] = self.current_history
            return str(user_guess) + ": " + str(bulls) + " bulls and " + str(cows) + " cows. \n" \
                                                                                     "Congratulations, you win!"
        else:
            return str(user_guess) + ": " + str(bulls) + " bulls and " + str(cows) + " cows"

    # Clears current and total game history
    def clear(self):
        """ Clears current and total game history
        Return:
            String: History cleared
        """
        self.current_history.clear()
        global total_history
        total_history.clear()
        global total_games
        total_games = 0
        return "History cleared"

    # Resets current game history
    def reset(self):
        """resets current game history
        Return:
            String: Game reset
        """
        self.current_history.clear()
        self.hidden_sequence = self.generate_hidden_sequence()
        self.game_state = "New game."
        return "Game reset"

    @staticmethod
    def display_game_name():
        """displays game name

        Return: 
            string: Mastermind
        """
        return "Mastermind"

    @staticmethod
    def get_subdir() -> str:
        """displays the subdirectory name for the game

        Return:
            string: mastermind
        """
        return 'mastermind'

    @staticmethod
    def get_help():
        """displays the help instructions
        Return:
            String: type a 4 digit number to guess a 4 digit secret number" 
               "Each turn the game will return how close your guess was " 
               "bulls are numbers that are the correct value in the correct position" 
               "cows are numbers that are the correct value but not in the correct position"

        """
        return "type a 4 digit number to guess a 4 digit secret number" \
               "Each turn the game will return how close your guess was " \
               "bulls are numbers that are the correct value in the correct position" \
               "cows are numbers that are the correct value but not in the correct position"


