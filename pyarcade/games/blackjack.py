from pyarcade.games.card import Rank
from pyarcade.games.deck import Deck
from pyarcade.games.player import Player


# Count all aces as 11 for now.
# TODO: Implement user choosing ace value to be 1 or 11.
class Blackjack:
    """Represent a game of blackjack, controlling game flow.
    """
    def __init__(self):
        self.user = Player()
        self.house = Player()
        self.game_state = "New Game"
        self.setup()

    def setup(self) -> None:
        """Set up the game by dealing the player and the house two cards each.
        """
        self.deck = Deck()
        self.deck.shuffle()
        self.user.add_to_hand(self.deck.draw())
        self.house.add_to_hand(self.deck.draw())
        self.user.add_to_hand(self.deck.draw())
        self.house.add_to_hand(self.deck.draw())

    def hit(self, player: Player) -> None:
        """Deal a card to a player.

        Args:
            player (Player): player who gets card
        """
        player.add_to_hand(self.deck.draw())

    def reset(self) -> str:
        self.clear()
        self.setup()
        return "Game reset"

    def clear(self) -> str:
        """Reset the game by clearing all player hands.
        """
        self.house.clear_hand()
        self.user.clear_hand()
        self.game_state = "New Game"
        return "History cleared"

    @staticmethod
    def calculate_current_sum(player: Player) -> int:
        """Calculate the sum of the card values in a player's hand.
        """
        curr_sum = 0
        for card in player.get_cards():
            if card.get_rank() == Rank.ACE:
                curr_sum += 11
            elif card.is_face_card():
                curr_sum += 10
            else:
                curr_sum += card.get_rank().value

        return curr_sum

    def bust(self) -> str:
        """updates game state and returns loss string 
        """
        self.game_state = "Game over."
        return "BUST"

    def win(self) -> str:
        """updates game state and returns win string
        """
        self.game_state = "Game over."
        return "WIN BABY"

    def tie(self) -> str:
        self.game_state = "Game over."
        return "TIE"

    # defines win conditions given both user sum and hand sum
    def win_condition(self) -> str:
        """Check if the user has won or lost when the game is ending.

        Returns:
            str: result of the game
        """
        user_sum = self.calculate_current_sum(self.user)
        house_sum = self.calculate_current_sum(self.house)

        if user_sum > 21 and house_sum > 21:
            return self.tie()

        if user_sum > 21:
            return self.bust()

        if house_sum > 21:
            return self.win()

        if user_sum > house_sum:
            return self.win()

        else:
            self.clear()
            return self.bust()

    def check_if_bust(self, user_sum: int, house_sum: int) -> str:
        """
        checks if after a turn the user has busted or not. Used when input is hit
        """
        if user_sum > 21:
            self.clear()
            return self.bust()

        elif user_sum == 21:
            self.clear()
            return self.win()
        elif house_sum > 21:
            self.clear()
            return self.win()

        return ""

    def next_state(self, decision: str) -> str:
        """Play out one turn of blackjack given the user decision to hit or
        stand.

        Args:
            decision (str): user decision to hit or stand

        Returns:
            str: next game state
        """
        win_status = ""
        house_sum = self.calculate_current_sum(self.house)
        user_sum = self.calculate_current_sum(self.user)

        # user hits
        if decision == "hit":
            self.hit(self.user)
            user_sum = self.calculate_current_sum(self.user)
            win_status = self.check_if_bust(user_sum, house_sum)

        # user stands
        elif decision == "stand":
            # dealer must hit under 17
            while house_sum < 17:
                self.hit(self.house)
                house_sum = self.calculate_current_sum(self.house)

            win_status = self.win_condition()

        elif decision == "help" :
            return "Welcome to blackjack. Please type in your next move." \
                   " Acceptable commands are hit or stand. To quit type quit. To see this help menu type help."

        elif decision == "quit":
            return "QUIT"

        # return the decision
        return self.display_state(win_status)

    def display_state(self, win_status: str) -> str:
        """[summary]

        Args:
            win_status (str): [description]
        """
        user_hand_sum = self.calculate_current_sum(self.user)
        house_hand_sum = self.calculate_current_sum(self.house)

        # strings to display
        user_hand_str = "CURRENT HAND: " + str(user_hand_sum)
        house_hand_str = "HOUSE HAND: " + str(house_hand_sum)

        return user_hand_str + "\n" + house_hand_str + "\n" + win_status

    def start_game(self, decision: str):
        result = ["BUST", "WIN BABY", "TIE", "QUIT"]
        if decision not in result:
            decision = self.next_state(decision)
        return decision

    @staticmethod
    def get_name():
        return 'Blackjack'

    @staticmethod
    def get_subdir() -> str:
        return 'blackjack'

    @staticmethod
    def get_help():
        return "You are originally dealt two cards and one card from the houses hand will be flipped up." \
                "You have the choice to either have another card dealt to you (hit) or to stick with " \
               "your cards (stand). If your hand's sum is closest to twenty-one then you win, if the sum " \
               "is over twenty-one, you lose (bust), or if the sum is exactly twenty-one you win (blackjack)." \
               "(User input should be in the form of either: Hit or Stand))"
