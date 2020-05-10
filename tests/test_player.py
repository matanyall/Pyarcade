import pytest
from pyarcade.games.card import Rank, Suit, Card
from pyarcade.games.player import Player
import unittest


@pytest.mark.local
class PlayerTestCase(unittest.TestCase):
    def test_remove_from_hand(self):
        pass

    def test_has(self):
        pass

    def test_get_cards(self):
        cards = [Card(Rank.ACE, Suit.SPADES), Card(Rank.ACE, Suit.HEARTS),
                 Card(Rank.KING, Suit.SPADES), Card(Rank.QUEEN, Suit.DIAMONDS)]
        p1 = Player(cards)
        self.assertEqual(len(p1.get_cards()), 4)
        self.assertEqual(len(p1.get_cards(Rank.ACE)), 2)
        self.assertEqual(len(p1.get_cards(Suit.SPADES)), 2)
        self.assertEqual(len(p1.get_cards(Suit.CLUBS)), 0)

    def test_show_hand(self):
        pass
