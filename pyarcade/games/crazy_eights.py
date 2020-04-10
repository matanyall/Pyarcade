from __future__ import annotations
from typing import Optional, List
from collections import deque
import random
from pyarcade.games.card import Rank, Suit, Card
from pyarcade.games.player import Player


class CrazyEights:
    """Represent a crazy eights game.

    Args:
        num_players (int): number of players from [2, 7].
    """

    def __init__(self, num_players: int):
        # Set up the game.
        self.setup_game(num_players)
        self.curr_suit = Suit.SPADES  # suit choice after an eight is played

        # Keep track of the game history.
        self.game_hist = []
        self.game_state = "New game."

    def setup_round(self, num_players: int) -> CrazyEights:
        """Set up the game by making a deck, shuffling it, dealing cards,
        making a discard, flipping over the top card, and creating the
        round points.

        Args:
            num_players (int): number of players

        Returns:
            CrazyEights: game after the setup is complete
        """
        for player in self.players.values():
            player.clear_hand()  # empty the players' hands from prev rounds
        self.new_deck() if len(self.players) <= 5 else self.new_deck(2)
        self.shuffle_deck()
        num_cards = 5 if len(self.players) > 2 else 7
        self.deal(num_cards)
        self.discard = []
        self.discard.append(self.deck.popleft())
        self.pts = [0] * num_players

    def setup_game(self, num_players: int) -> CrazyEights:
        """Set up the game by creating the players, creating the round history,
        and completing round setup.

        Args:
            num_players (int): number of players the game will have

        Returns:
            CrazyEights: game after being set up
        """
        # Create the players, numbering them from [1, num_players]. The user
        # is player 1.
        self.players = {}
        for n in range(num_players):
            # Note that constructing with [] is needed to block pointer aliases
            self.players[n + 1] = Player([])

        # Create the round history.
        self.round_hist = []

        # Set up for the first round.
        self.setup_round(num_players)

        return self

    def new_deck(self, num_decks: Optional[int] = 1) -> CrazyEights:
        """Create a new deck of cards composed of a number of 52-card decks.

        Args:
            num_decks (Optional[int], optional): number of 52-card decks to
            use. Defaults to 1.

        Returns:
            CrazyEights: game after the deck has been created
        """
        self.deck = deque([])
        for suit in Suit:
            for rank in Rank:
                new_card = Card(rank, suit)
                for i in range(num_decks):
                    self.deck.append(new_card)
        return self

    def shuffle_deck(self) -> CrazyEights:
        """Shuffle the game's current deck of cards.

        Returns:
            CrazyEights: game after the deck has been shuffled
        """
        for curr_idx in reversed(range(len(self.deck))):
            swap_idx = random.randint(0, curr_idx)
            self.deck[curr_idx], self.deck[swap_idx] = \
                self.deck[swap_idx], self.deck[curr_idx]
        return self

    def deal(self, num_cards: Optional[int] = -1) -> CrazyEights:
        """Deal the cards in the deck out to the players.

        Args:
            num_cards (Optional[int], optional): number of cards to deal each
            player. If less than zero or greater than the deck size, deal out
            all the cards in the deck. Defaults to -1 (deal whole deck).

        Returns:
            CrazyEights: game after the cards have been dealt
        """
        cards_to_deal = num_cards * len(self.players)
        if cards_to_deal < 0 or cards_to_deal > len(self.deck):
            cards_to_deal = len(self.deck)

        for card_count in range(cards_to_deal):
            player_to_deal = (card_count % len(self.players)) + 1
            card = self.deck.popleft()
            self.players.get(player_to_deal).add_to_hand(card)

        return self

    def show_player_hand(self, player_num: int) -> str:
        """Show the current hand of a player.

        Args:
            player_num (int): number of the player's hand to show

        Returns:
            str: hand of the player; empty string if player doesn't exist
        """
        if player_num < 1 or player_num > len(self.players):
            return ''
        return self.players.get(player_num).show_hand()

    def draw(self, player_num: int) -> CrazyEights:
        """Draw a card from the top of the deck and place it into a player's
        hand.

        Args:
            player (int): number of the player who is drawing a card

        Returns:
            CrazyEights: game after the player has drawn
        """
        if player_num < 1 or player_num > len(self.players):
            return self

        if not self.deck and len(self.discard) <= 1:
            self.reset_round()
            return self

        if not self.deck:
            top_card = self.discard.pop()
            self.deck.extend(self.discard)
            self.discard.clear()
            self.discard.append(top_card)
            self.shuffle_deck()

        card = self.deck.popleft()
        self.players.get(player_num).add_to_hand(card)
        return self

    def play(self, player_num: int, card_to_play: Card,
             set_suit: Optional[Suit] = Suit.SPADES) -> bool:
        """Play a specific card, if possible.

        Args:
            player_num (int): number of the player playing the card. Defaults
            to player 1, the user.
            card_to_play (Card): desired card to play
            set_suit (Optional[Suit], optional): suit to change the play to
            if the card being played is an eight. Defaults to spades.

        Returns:
            bool: True if the card was played, and False otherwise
        """
        player = self.players.get(player_num)
        if player.has(card_to_play) and self.playable(card_to_play):
            player.remove_from_hand(card_to_play)
            self.discard.append(card_to_play)

            if not player.has_cards():
                self.game_state = "Round {}".format(str(len(self.round_hist) + 1))
                self.reset_round()

            if card_to_play.get_rank() == Rank.EIGHT:
                self.curr_suit = set_suit

            return True
        return False

    def show_top_card(self):
        return self.discard[-1].__str__()

    def playable(self, card_to_play: Card) -> bool:
        """Checks whether a card can be played.

        Args:
            card_to_play (Card): card to try to play

        Returns:
            bool: whether the card can be played or not
        """
        top_card = self.discard[-1]
        tc_suit = self.get_top_card_suit()  # suit might be set differently

        # Check the conditions to be met for the card to be playable.
        return (card_to_play.get_rank() == top_card.get_rank() or
                card_to_play.get_suit() == tc_suit or
                card_to_play.get_rank() == Rank.EIGHT)

    def get_top_card_suit(self) -> Suit:
        """Get the top card's suit, as it might be set by an eight.

        Returns:
            Suit: suit of top card in discard
        """
        tc = self.discard[-1]
        tc_suit = tc.get_suit()
        # TODO: add prot for when card flipped to start game is an eight
        if tc.get_rank() == Rank.EIGHT:
            tc_suit = self.curr_suit
        return tc_suit

    def play_options(self, player_num: int) -> List[Card]:
        """Find the cards in a player's hand that can be played.

        Args:
            player_num (int): player number

        Returns:
            List[Card]: cards in the player's hand that are viable
        """
        top_card = self.discard[-1]
        tc_suit = self.get_top_card_suit()

        player = self.players.get(player_num)
        same_rank = player.get_cards(top_card.get_rank())
        same_suit = player.get_cards(tc_suit)
        eights = player.get_cards(Rank.EIGHT)

        cards = same_rank + same_suit + eights
        return cards

    def turn(self, player_num: int) -> Card:
        """Play out a player's turn using automated choices.

        Args:
            player_num (int): number of the player whose turn it is

        Returns:
            Card: card that the player plays
        """
        while True:
            # Try to play the first possible card.
            card_ops = self.play_options(player_num)
            if card_ops:
                self.play(player_num, card_ops[0])
                break
            # Draw a card if none could be played.
            else:  # TODO: check behavior if game ends off of emptying deck
                self.draw(player_num)

    def reset_round(self) -> CrazyEights:
        """Reset the round, storing it into the game's round history.

        Returns:
            CrazyEights: game after the round has been reset
        """
        # Store the game state in the round history.
        self.round_hist.append(self.players)

        # Count each player's points.
        for n in self.players:
            player = self.players.get(n)
            for card in player.get_cards():
                card_pts = card.get_rank().value
                if card.get_rank() == Rank.EIGHT:
                    card_pts = 50
                if card.get_rank() > Rank.TEN:
                    card_pts = 10
                self.pts[n - 1] += card_pts

        # The player(s) with the lowest points won. Add the differences between
        # their points and each of the other players' points to their scores.
        min_score = min(self.pts)
        winners = []
        total_pts_diff = 0
        for i in range(len(self.players)):
            if self.pts[i] == min_score:
                winners.append(i)
            if self.pts[i] > min_score:
                total_pts_diff += self.pts[i] - min_score

        for i in range(len(winners)):
            winner = self.players.get(i + 1)
            winner.increase_score(total_pts_diff)

        # Reset the round by setting up a new round and return.
        self.setup_round(len(self.players))
        return self

    def reset(self, num_players: Optional[int] = None) -> str:
        """Reset the game, storing its current state in the game history.

        Args:
            num_players (Optional[int], optional): number of players to start
            the new game with. Defaults to None (use current number of players)

        Returns:
            CrazyEights: game after being reset
        """
        self.game_state = "New game."
        self.reset_round()  # reset round to store current round into hist
        self.game_hist.append((self.players, self.round_hist))
        if num_players:
            self.setup_game(num_players)
        else:
            self.setup_game(len(self.players))
        return "Game reset"

    def clear(self) -> str:
        """Reset the current game and clear all game history.

        Returns:
            CrazyEights: game after being cleared
        """
        self.reset()
        self.game_hist.clear()
        return "History cleared"
