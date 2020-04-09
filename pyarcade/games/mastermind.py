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

    def __init__(self, width: Optional[int] = 4, max_range: Optional[int] = 10):
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

    def evaluate(self, user_guess: List[int]) -> Dict[int, int]:
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

        for idx in range(len(user_guess)):
            if user_guess[idx] == self.hidden_sequence[idx]:
                evaluation[user_guess[idx]] = 1
            elif user_guess[idx] in self.hidden_sequence:
                evaluation[user_guess[idx]] = 0
                exact_match = False
            else:
                evaluation[user_guess[idx]] = -1
                exact_match = False

        self.current_history[tuple(user_guess)] = evaluation

        if exact_match:
            total_history[total_games] = self.current_history

        return evaluation

    # Clears current and total game history
    def clear(self):
        self.current_history.clear()
        global total_history
        total_history.clear()
        global total_games
        total_games = 0

    # Resets current game history
    def reset(self):
        self.current_history.clear()
        self.hidden_sequence = self.generate_hidden_sequence()
