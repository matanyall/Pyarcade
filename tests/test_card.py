import pytest
from pyarcade.games.card import Rank, Suit, Card
import unittest


@pytest.mark.local
class CardTestCase(unittest.TestCase):
    def test_eq(self):
        card1 = Card(Rank.ACE, Suit.SPADES)
        card2 = Card(Rank.ACE, Suit.SPADES)
        card3 = Card(Rank.ACE, Suit.CLUBS)
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)

    def test_str(self):
        card1 = Card(Rank.ACE, Suit.SPADES)
        self.assertEqual(card1.__str__(), 'ace of spades')

    def test_get_rank(self):
        card1 = Card(Rank.ACE, Suit.SPADES)
        self.assertEqual(card1.get_rank(), Rank.ACE)

    def test_get_suit(self):
        card1 = Card(Rank.ACE, Suit.SPADES)
        self.assertEqual(card1.get_suit(), Suit.SPADES)
