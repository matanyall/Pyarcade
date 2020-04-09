from pyarcade.games.mastermind import Mastermind
from pyarcade.games.minesweeper import Minesweeper
from pyarcade.games.card import Rank, Suit, Card
from pyarcade.games.crazy_eights import CrazyEights
import re

MASTERMIND_WIDTH = 4

CRAZY_EIGHTS_NUM_PLAYERS = 4
CRAZY_EIGHTS_PLAYER_NUM = 1


class InputSystem:

    def __init__(self):
        self.mastermind_game = Mastermind()
        self.minesweeper_game = Minesweeper()
        self.crazy_eights_game = CrazyEights(CRAZY_EIGHTS_NUM_PLAYERS)

    def handle_game_input(self, game_name: str, user_choice: str):
        if game_name == "Mastermind":
            return self.handle_mastermind_input(user_choice)
        elif game_name == "Minesweeper":
            return self.handle_minesweeper_input(user_choice)
        elif game_name == "Crazy Eights":
            return self.handle_crazy_eights_input(user_choice)
        else:
            return "Invalid game provided."

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

            if len(guess_output) == MASTERMIND_WIDTH:
                return self.mastermind_game.evaluate(guess_output)
        return "Invalid input. Input should be of the form \"####\""

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

        return "Invalid input. User should specify an x and y coordinate: \"#,#\""

    def handle_card(self, user_card: str):
        user_card = user_card.split(",")

        for rank in Rank:
            card_rank = "rank.{}".format(user_card[0].lower())
            for suit in Suit:
                card_suit = "suit.{}".format(user_card[1].lower())

                if str(rank).lower() == card_rank and str(suit).lower() == card_suit:
                    return Card(rank, suit)
        return None

    def handle_crazy_eights_input(self, card_input: str) -> str:
        if card_input == 'draw':
            self.crazy_eights_game.draw(CRAZY_EIGHTS_PLAYER_NUM)
            return self.crazy_eights_game.show_player_hand(CRAZY_EIGHTS_PLAYER_NUM)

        card = self.handle_card(card_input)

        if card:
            not_str = 'not ' if not self.crazy_eights_game.play(card) else ''
            return 'card {} was '.format(str(card)) + not_str + 'played'
        else:
            return "Invalid input. User should specify either to draw or which card to place (Ex: Eight,Spades)"
