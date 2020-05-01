from pyarcade.games.card import Rank
from pyarcade.games.deck import Deck


# Count aces as 11 for now.
class Blackjack:
    """Represent a game of blackjack, controlling game flow.
    """
    def __init__(self):
        self.user_hand = []
        self.house_hand = []
        self.game_state = "New Game"
        self.setup()

    def setup(self):
        """
        sets up the game for player by drawing two cards for the player and the house
        """
        self.deck = Deck()
        self.deck.shuffle()
        self.user_hand.append(self.deck.draw())
        self.house_hand.append(self.deck.draw())
        self.user_hand.append(self.deck.draw())
        self.house_hand.append(self.deck.draw())

    def hit(self, hand: list):
        hand.append(self.deck.draw())

    def clear(self):
        """
        clears deck and hands for clean slate
        """
        self.house_hand.clear()
        self.user_hand.clear()
        self.game_state = "New Game"
        return "History cleared"

    def reset(self):
        self.clear()
        self.setup()
        return "Game reset"

    # calculates sum of cards in hand
    @staticmethod
    def calculate_current_sum(hand: list) -> int:
        """
        calculates the total of the users hand
        """
        curr_sum = 0
        for card in hand:
            if card.get_rank() == Rank.ACE:
                curr_sum += 11
            elif card.is_face_card():
                curr_sum += 10
            else:
                curr_sum += card.get_rank().value

        return curr_sum

    def bust(self) -> str:
        self.game_state = "Game over."
        return "BUST"

    def win(self) -> str:
        self.game_state = "Game over."
        return "WIN BABY"

    def tie(self) -> str:
        self.game_state = "Game over."
        return "TIE"

    # defines win conditions given both user sum and hand sum
    def win_condition(self, user_sum: int, house_sum: int) -> str:
        """
        checks if the user has won or lost, this is used when the player stands and the game is ending
        """
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
    # one turn of blackjack
    def next_state(self, user_hand: list, house_hand: list, decision: str) -> str:

        """
        goes through one turn of blackjack based on input hit or stand
        """
        win_status = ""
        house_sum = self.calculate_current_sum(house_hand)
        user_sum = self.calculate_current_sum(user_hand)

        # user hits
        if decision == "hit":
            self.hit(user_hand)
            user_sum = self.calculate_current_sum(user_hand)
            win_status = self.check_if_bust(user_sum, house_sum)
        
        # user stands
        elif decision == "stand":

            # dealer must hit under 17
            while house_sum < 17:
                self.hit(house_hand)
                house_sum = self.calculate_current_sum(house_hand)
            
            win_status = self.win_condition(user_sum, house_sum)

        elif decision == "help" :
            return "Welcome to blackjack. Please type in your next move." \
                   " Acceptable commands are hit or stand. To quit type quit. To see this help menu type help."

        elif decision == "quit":
            return "QUIT"

        # return the decision
        return self.display_state(user_sum, house_sum, win_status)

    def display_state(self, user_hand_sum: int, house_hand_sum: int, win_status: str):
        # strings to display

        user_hand_str = "CURRENT HAND: " + str(user_hand_sum)
        house_hand_str = "HOUSE HAND: " + str(house_hand_sum)

        return user_hand_str + "\n" + house_hand_str + "\n" + win_status

    def start_game(self, decision: str):

        #self.setup()
        result = ["BUST", "WIN BABY", "TIE", "QUIT"]
        if decision not in result:
            decision = self.next_state(self.user_hand, self.house_hand, decision)
        return decision

    @staticmethod
    def display_game_name():
        return "BlackJack"

    @staticmethod
    def display_help():
        return "You are originally dealt two cards and one card from the houses hand will be flipped up." \
                "You have the choice to either have another card dealt to you (hit) or to stick with " \
               "your cards (stand). If your hand's sum is closest to twenty-one then you win, if the sum " \
               "is over twenty-one, you lose (bust), or if the sum is exactly twenty-one you win (blackjack)." \
               "(User input should be in the form of either: Hit or Stand))"
