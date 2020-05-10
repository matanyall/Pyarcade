from pyarcade.games.mastermind import Mastermind
from pyarcade.games.minesweeper import Minesweeper
from pyarcade.games.card import Rank, Suit, Card
from pyarcade.games.crazy_eights import CrazyEights
from pyarcade.games.blackjack import Blackjack
import re

_SUPPORTED_GAMES = {
    'blackjack': 'Blackjack',
    'crazy_eights': 'Crazy Eights',
    'mastermind': 'Mastermind',
    'minesweeper': 'Minesweeper'
}

MASTERMIND_WIDTH = 4
CRAZY_EIGHTS_NUM_PLAYERS = 4
CRAZY_EIGHTS_PLAYER_NUM = 1


class InputSystem:
    """Class that handles input for all games 
    """

    def __init__(self):
        self.mastermind_game = Mastermind()
        self.minesweeper_game = Minesweeper()
        self.crazy_eights_game = CrazyEights(CRAZY_EIGHTS_NUM_PLAYERS)
        self.blackjack_game = Blackjack()
        self.game_to_load = None
        self.current_game = None

    @staticmethod
    def get_supported_games():
        return _SUPPORTED_GAMES

    def get_current_game(self):
        """getter for current game

        Returns:
            game: return current game which could be any of the games in pyarcade 
        """
        return self.current_game

    def set_current_game(self, game):
        """setter for current game

        Args:
            game: is the game that you are setting current game to could be 
                    any type of game within pyarcade
        """
        self.current_game = game

    def set_game_to_load(self, game):
        """setter for game to load

        Args:
            game: is the game that you are setting game to load to could be 
                    any type of game within pyarcade
        """
        self.game_to_load = game

    def handle_game_input(self, game_name: str, user_input: str):
        """Handles input given game name (mastermind, minesweeper, crazy eights, blackjack, etc) and user input and returns the correct output based on which
        game and the option that is selected. 

        Args:
            game_name (str): name of the game to check input against
            user_input (str): user input representing which choice from main menu options is chosen
        
        Returns:
            
        """
        if game_name.lower() == "mastermind":
            if user_input.lower() == "new game":
                self.mastermind_game = Mastermind()
                self.current_game = self.mastermind_game
                return "\nMastermind\n"
            elif user_input.lower() == "continue":
                return "\nMastermind\n"
            return self.handle_mastermind_input(user_input)
        elif game_name.lower() == "minesweeper":
            if user_input.lower() == "new game":
                self.minesweeper_game = Minesweeper()
                self.current_game = self.minesweeper_game
                return "Minesweeper\n" + self.minesweeper_game.draw_board()
            elif user_input.lower() == "continue":
                return "Minesweeper\n" + self.minesweeper_game.draw_board()
            return self.handle_minesweeper_input(user_input)
        elif game_name.lower() == "crazy eights":
            if user_input.lower() == "new game":
                self.crazy_eights_game = CrazyEights(CRAZY_EIGHTS_NUM_PLAYERS)
                self.current_game = self.crazy_eights_game
                return "\nCrazy Eights\n\n" + self.crazy_eights_game.game_state + "\nTop Card: " \
                       + self.crazy_eights_game.show_top_card() + " \n\nPlayer Hand: \n" \
                       + self.crazy_eights_game.show_player_hand(CRAZY_EIGHTS_PLAYER_NUM) + "\n"
            elif user_input.lower() == "continue":
                return "\nCrazy Eights\n\n" + self.crazy_eights_game.game_state + "\nTop Card: " \
                       + self.crazy_eights_game.show_top_card() + " \n\nPlayer Hand: \n" \
                       + self.crazy_eights_game.show_player_hand(CRAZY_EIGHTS_PLAYER_NUM) + "\n"
            return self.handle_crazy_eights_input(user_input)
        elif game_name.lower() == "blackjack":
            if user_input.lower() == "new game":
                self.blackjack_game = Blackjack()
                self.current_game = self.blackjack_game
                return "\n Blackjack\n" + "\nHouse's revealed card: " \
                       + str(self.blackjack_game.house.get_cards()[0].get_rank().value) + " \n\nPlayer Hand: \n" \
                       + str(self.blackjack_game.user.get_cards()[0].get_rank().value) + ", " \
                       + str(self.blackjack_game.user.get_cards()[1].get_rank().value) + "\n"
            elif user_input.lower() == "continue":
                win_status = self.blackjack_game.win_condition()
                return self.blackjack_game.display_state(win_status)
            return self.handle_blackjack_input(user_input)
        else:
            return "Invalid game provided."

    def handle_mastermind_input(self, guess_input):
        """ Accesses the mastermind game and runs mastermind logic based on user input and returns result for
        start.py to print out.This function acts as a handler that calls the functions associated with the mastermind to allow the player to progress in the game or execute game specific menu options
        chosen and then returns the output.
            
        Args:
            guess_input (str): input that decides which menu option to take or guess to evaluate
        Returns:
            hidden_sequence List[int]: A sequence of integers to be guessed by the player.
        """
        if type(guess_input) == str:
            if guess_input.lower() == "clear":
                return self.mastermind_game.clear()
            if guess_input.lower() == "reset":
                return self.mastermind_game.reset()
            if guess_input.lower() == "help":
                return self.mastermind_game.get_help()
            if guess_input.lower() == "state":
                return self.mastermind_game.game_state
            if guess_input.lower() == "save":
                output = self.mastermind_game
                return output
            if guess_input.lower() == "load":
                self.mastermind_game = self.game_to_load
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
        """ Accesses the minesweeper game and runs minesweeper logic based on user input and returns result for
        start.py to print out.This function acts as a handler that calls the functions associated with minesweeper to allow the player to progress in the game or execute game specific menu options
        chosen and then returns the output.
            
        Args:
            location_input (str): location of desired move represented as a string or menu option depending on format
        Returns:
            board_str (str): a string representation of the minesweeper board 
        """
        if type(location_input) == str:
            two_comma_separated_digits_regex = r"^\d,\d$"
            if re.search(two_comma_separated_digits_regex, location_input):
                location_guess = location_input.split(',')
                if self.minesweeper_game.is_valid(int(location_guess[0]), int(location_guess[1])):
                    return self.minesweeper_game.make_move([int(location_guess[0]), int(location_guess[1])])
                else:
                    return "Guess is out of bounds. Please provide input within the bounds of the grid."
            elif location_input.lower() == "reset":
                output = self.minesweeper_game.reset_game() + "\n"
                return output + self.minesweeper_game.draw_board()

            elif location_input.lower() == "save":
                output = self.minesweeper_game
                return output

            elif location_input.lower() == "load":
                self.minesweeper_game = self.game_to_load
                return self.minesweeper_game.draw_board()

            elif location_input.lower() == "clear":
                return self.minesweeper_game.clear_game_history() + "\n" + self.minesweeper_game.draw_board()
            elif location_input.lower() == "state":
                return self.minesweeper_game.game_state
            elif location_input.lower() == "help":
                return self.minesweeper_game.get_help()

        return "Invalid input. User should specify an x and y coordinate: \"<row>,<col>\""

    @staticmethod
    def handle_card(user_card: str):
        """ Finds a corresponding card based on user input and returns that card of type card. If none exist
        it returns None
        Args: 
            user_card (str): string representation of Users card played

        Return:
            Card: card with rank and suit specified
            None
        """
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
        """Handles input varying from game menu options such as help, save, clear and game options such as draw
         Accesses the crazy eights game and runs crazy eights logic based on user input and returns result for
        start.py to print out
            
        Args:
            card_input (str): 
        Returns:
            String: returns what the last card played was in the form of a string 
        """
        if card_input.lower() == "help":
            return self.crazy_eights_game.get_help()
        if card_input.lower() == "clear":
            return self.crazy_eights_game.clear()
        if card_input.lower() == "state":
            return self.crazy_eights_game.game_state
        if card_input.lower() == "save":
            output = self.crazy_eights_game
            return output
        if card_input.lower() == "load":
            self.crazy_eights_game = self.game_to_load
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
            return invalid_str + "\nTop Card: " + self.crazy_eights_game.show_top_card() \
                   + "\n\nPlayer Hand: \n" + self.crazy_eights_game.show_player_hand(CRAZY_EIGHTS_PLAYER_NUM)

    def handle_blackjack_input(self, user_input: str) -> str:
        """ This Accesses the blackjack game and runs blackjack logic based on user input and returns result for
        start.py to print out. This function acts as a handler that calls the functions associated with blackjack to allow the player to progress in the game or execute game specific menu options
        chosen and then returns the output.
            
        Args:
            user_input: input from user varying from menu options to game options such as hit or stand
        
        Returns:
            String: returns current state of user and house hands 
        """

        if user_input.lower() == "help":
            return self.blackjack_game.get_help()
        if user_input.lower() == "reset":
            return self.blackjack_game.reset()
        if user_input.lower() == "clear":
            return self.blackjack_game.clear()
        if user_input.lower() == "state":
            return self.blackjack_game.game_state
        if user_input.lower() == "save":
            output = self.blackjack_game
            return output

        if user_input.lower() == "load":
            self.blackjack_game = self.game_to_load
            win_status = self.blackjack_game.win_condition()
            return self.blackjack_game.display_state(win_status)
        if user_input.lower() == "hit" or user_input.lower() == "stand":
            return self.blackjack_game.start_game(user_input)
        else:
            return "Invalid input. User should specify hit or stand."
