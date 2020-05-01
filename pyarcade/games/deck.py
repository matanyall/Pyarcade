from __future__ import annotations
from typing import Optional, List
from collections import deque
import random
from pyarcade.games.card import Rank, Suit, Card


class Deck:
    """Represent a deck of playing cards composed of a number of 52-card decks.

    Args:
        num_decks (Optional[int], optional): number of 52-card decks to
        use. Defaults to 1.
    """
    def __init__(self, num_decks: Optional[int] = 1):
        # Create the deck.
        self._cards = deque([])
        for suit in Suit:
            for rank in Rank:
                new_card = Card(rank, suit)
                for i in range(num_decks):
                    self._cards.append(new_card)

    def shuffle(self) -> Deck:
        """Shuffle the deck using random.shuffle, which uses the Fisher-Yates
        algorithm.

        Returns:
            Deck: deck after shuffling
        """
        random.shuffle(self._cards)
        return self

    def draw(self) -> Card:
        """Draw a card off the top of the deck.

        Returns:
            Card: card drawn
        """
        return self._cards.popleft()

    def size(self) -> int:
        """Get the number of cards in the deck.

        Returns:
            int: number of cards in the deck
        """
        return len(self._cards)

    def is_empty(self) -> bool:
        """Determine whether the deck has no cards.

        Returns:
            bool: whether the deck is empty or not
        """
        return self.size() == 0

    def add_cards(self, cards_to_add: List[Card]) -> Deck:
        """Add cards to the bottom of the deck.

        Args:
            cards_to_add (List[Card]): cards to be added to the bottom of the
            deck

        Returns:
            Deck: deck after the cards are added
        """
        self._cards.extend(cards_to_add)
