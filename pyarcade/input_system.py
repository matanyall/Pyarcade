from pyarcade.games.mastermind import Mastermind
from pyarcade.games.minesweeper import Minesweeper
from pyarcade.games.card import Rank, Suit, Card
from pyarcade.games.crazy_eights import CrazyEights
from pyarcade.games.BlackJack import BlackJack
import re

MASTERMIND_WIDTH = 4

CRAZY_EIGHTS_NUM_PLAYERS = 4
CRAZY_EIGHTS_PLAYER_NUM = 1


class InputSystem:

    def __init__(self):
        self.mastermind_game = Mastermind()
        self.minesweeper_game = Minesweeper()
        self.crazy_eights_game = CrazyEights(CRAZY_EIGHTS_NUM_PLAYERS)
        self.blackjack_game = BlackJack()

    def handle_game_input(self, game_name: str, user_input: str):
        if game_name.lower() == "mastermind":
            if user_input.lower() == "new game":
                self.mastermind_game = Mastermind()
                return "\nMastermind\n"
            return self.handle_mastermind_input(user_input)
        elif game_name.lower() == "minesweeper":
            if user_input.lower() == "new game":
                self.minesweeper_game = Minesweeper()
                return "\nMinesweeper\n\n" + self.minesweeper_game.draw_board() + "\n"
            return self.handle_minesweeper_input(user_input)
        elif game_name.lower() == "crazy eights":
            if user_input.lower() == "new game":
                self.crazy_eights_game = CrazyEights(CRAZY_EIGHTS_NUM_PLAYERS)
                return "\nCrazy Eights\n\n" + self.crazy_eights_game.game_state + "\nTop Card: " \
                       + self.crazy_eights_game.show_top_card() + " \n\nPlayer Hand: \n" \
                       + self.crazy_eights_game.show_player_hand(CRAZY_EIGHTS_PLAYER_NUM) + "\n"
            return self.handle_crazy_eights_input(user_input)
        elif game_name.lower() == "blackjack":
            if user_input.lower() == "new game":
                self.blackjack_game = BlackJack()
                return "\n Blackjack\n" + "\nHouse's revealed card: " \
                       + str(self.blackjack_game.house_hand[0].value) + " \n\nPlayer Hand: \n" \
                       + str(self.blackjack_game.user_hand[0].value) + ", " \
                       + str(self.blackjack_game.user_hand[1].value) + "\n"
            return self.handle_blackjack_input(user_input)
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
            if guess_input.lower() == "clear":
                return self.mastermind_game.clear()
            if guess_input.lower() == "reset":
                return self.mastermind_game.reset()
            if guess_input.lower() == "help":
                return self.mastermind_game.display_help()
            if guess_input.lower() == "state":
                return self.mastermind_game.game_state

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
            elif location_input.lower() == "reset":
                output = self.minesweeper_game.reset_game() + "\n"
                return output + self.minesweeper_game.draw_board()
            elif location_input.lower() == "clear":
                return self.minesweeper_game.clear_game_history()
            elif location_input.lower() == "state":
                return self.minesweeper_game.game_state
            elif location_input.lower() == "help":
                return self.minesweeper_game.display_help()

        return "Invalid input. User should specify an x and y coordinate: \"#,#\""

    @staticmethod
    def handle_card(user_card: str):
        user_card = user_card.split(",")
        if len(user_card) != 2:
            return None

        for rank in Rank:
            card_rank = "rank.{}".format(user_card[0].lower())
            for suit in Suit:
                card_suit = "suit.{}".format(user_card[1].lower())

                if str(rank).lower() == card_rank and str(suit).lower() == card_suit:
                    return Card(rank, suit)
        return None

    def handle_crazy_eights_input(self, card_input: str) -> str:
        if card_input.lower() == "help":
            return CrazyEights.display_help()
        if card_input.lower() == "clear":
            return self.crazy_eights_game.clear()
        if card_input.lower() == "state":
            return self.crazy_eights_game.game_state
        if card_input.lower() == "reset":
            output = self.crazy_eights_game.reset(CRAZY_EIGHTS_NUM_PLAYERS) + "\n" + self.crazy_eights_game.game_state
            return output + "\n\nTop Card: " + self.crazy_eights_game.show_top_card() + "\n\nPlayer Hand: \n" \
                   + self.crazy_eights_game.show_player_hand(CRAZY_EIGHTS_PLAYER_NUM)
        curr_state = self.crazy_eights_game.game_state

        if card_input == 'draw':
            self.crazy_eights_game.draw(CRAZY_EIGHTS_PLAYER_NUM)
            return "\nTop Card: " + self.crazy_eights_game.show_top_card() + "\n\nPlayer Hand: \n" \
                   + self.crazy_eights_game.show_player_hand(CRAZY_EIGHTS_PLAYER_NUM)

        card = self.handle_card(card_input)

        if card:
            not_str = 'not ' if not self.crazy_eights_game.play(CRAZY_EIGHTS_PLAYER_NUM, card) else ''
            game_output = 'card {} was '.format(str(card)) + not_str + 'played \nTop Card: ' \
                          + self.crazy_eights_game.show_top_card() + "\n\nPlayer Hand: \n" \
                          + self.crazy_eights_game.show_player_hand(CRAZY_EIGHTS_PLAYER_NUM)
            if curr_state != self.crazy_eights_game.game_state:
                score = self.crazy_eights_game.players.get(CRAZY_EIGHTS_PLAYER_NUM).get_score()
                return self.crazy_eights_game.game_state + "\nScore: " + str(score) + "\n" + game_output
            else:
                return game_output
        else:
            invalid_str = "Invalid input. User should specify either to draw or which card to place (Ex: Eight," \
                          "Spades)\n "
            return invalid_str + "\nTop Card: " + self.crazy_eights_game.show_top_card() + "\n\nPlayer Hand: \n" \
                          + self.crazy_eights_game.show_player_hand(CRAZY_EIGHTS_PLAYER_NUM)

    def handle_blackjack_input(self, user_input: str) -> str:

        if user_input.lower() == "help":
            return BlackJack.display_help()
        if user_input.lower() == "reset":
            return self.blackjack_game.reset()
        if user_input.lower() == "clear":
            return self.blackjack_game.clear()
        if user_input.lower() == "state":
            return self.blackjack_game.game_state
        if user_input.lower() == "hit" or user_input.lower() == "stand":
            return self.blackjack_game.start_game(user_input)
        else:
            return "Invalid input. User should specify hit or stand."
