from __future__ import annotations
from pyarcade.games.card import Rank, Card
from typing import Optional, List


class Player:
    """Represent a card game player.

    Args:
        cards (Optional[List[Card]], optional): cards to add to the player's
        hand. Defaults to [] (empty hand).
    """
    def __init__(self, cards: Optional[List[Card]] = []):
        self.hand = cards
        self.score = 0

    def add_to_hand(self, card: Card) -> Player:
        """Add a card to the player's hand.

        Args:
            card (Card): card to add

        Returns:
            Player: player with card added to their hand
        """
        self.hand.append(card)
        return self

    def remove_from_hand(self, card: Card) -> Player:
        """Remove a card from the player's hand.

        Args:
            card (Card): card to remove

        Returns:
            Player: player with card removed from their hand
        """
        for card_idx in range(len(self.hand)):
            if self.hand[card_idx] == card:
                self.hand.pop(card_idx)
                break
        return self

    def has(self, card: Card) -> bool:
        """Check whether the player has a certain card.

        Args:
            card (Card): card to check for in the player's hand

        Returns:
            bool: whether the card is present in the player's hand or not
        """
        return card in self.hand

    def has_cards(self) -> bool:
        """Checks whether the player has any cards.

        Returns:
            bool: whether the player has any cards in their hand or not
        """
        return bool(self.hand)  # force conversion here to encapsulate data

    def get_cards(self, rank_or_suit = None) -> List[Card]:
        """Get all the cards in the player's hand, or all with a certain rank
        or suit.

        Args:
            rank_or_suit: card rank or suit to match against

        Returns:
            List[Card]: cards in the player's hand, with the requested rank
            or suit if it was supplied
        """
        cards = []
        if rank_or_suit and isinstance(rank_or_suit, Rank):
            for card in self.hand:
                if card.get_rank() == rank_or_suit:
                    cards.append(card)
        elif rank_or_suit:  # isinstance(rank_or_suit, Suit) (we hope)
            for card in self.hand:
                if card.get_suit() == rank_or_suit:
                    cards.append(card)
        else:
            cards = self.hand
        return cards

    def show_hand(self) -> str:
        """Show the player's hand.

        Returns:
            str: representation of the cards in the player's hand
        """
        # TODO: sort the cards
        str_hand = ""
        for card in self.hand:
            str_hand += card.__str__() + "\n"

        return str_hand

    def clear_hand(self) -> Player:
        """Clear the player's hand of all cards.

        Returns:
            Player: player after their hand has been emptied
        """
        self.hand.clear()

    def get_score(self) -> int:
        """Get the player's score.

        Returns:
            int: player's score
        """
        return self.score

    def increase_score(self, pts: int) -> int:
        """Increase the player's score.

        Args:
            pts (int): points to increase the player's score by

        Returns:
            int: player's updated score after the increase
        """
        self.score += pts
        return self.get_score

    def decrease_score(self, pts: int) -> int:
        """Decrease the player's score.

        Args:
            pts (int): points to decrease the player's score by

        Returns:
            int: player's updated score after the decrease
        """
        self.score -= pts
        return self.get_score
