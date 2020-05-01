from pyarcade.games.ordered_enum import OrderedEnum
from enum import unique


@unique
class Suit(OrderedEnum):
    """OrderedEnum to represent all playing card suits.
    """
    SPADES = 0
    HEARTS = 1
    CLUBS = 2
    DIAMONDS = 3


@unique
class Rank(OrderedEnum):
    """OrderedEnum to represent all playing card ranks. The value of aces is
    one. Jokers are not included.
    """
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Card:
    """Represent a playing card with a suit and rank.

    Args:
        rank (Rank): playing card rank
        suit (Suit): playing card suit
    """
    def __init__(self, rank: Rank, suit: Suit):
        self.RANK = rank
        self.SUIT = suit

    def __eq__(self, other: object):
        return (isinstance(other, Card) and
                self.get_rank() == other.get_rank() and
                self.get_suit() == other.get_suit())

    def __str__(self):
        return self.get_rank().name.lower() + ' of ' +\
            self.get_suit().name.lower()

    def get_rank(self) -> Rank:
        return self.RANK

    def get_suit(self) -> Suit:
        return self.SUIT

    def is_face_card(self) -> bool:
        return self.RANK > Rank.TEN
