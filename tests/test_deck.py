import unittest

import pytest
from pyarcade.games.card import Rank, Suit, Card
from pyarcade.games.deck import Deck

_DECK_SZ = 52


@pytest.mark.local
class DeckTestCase(unittest.TestCase):
    def test_new_single_deck(self):
        deck = Deck()
        self.assertEqual(deck.size(), _DECK_SZ)

        as_card = Card(Rank.ACE, Suit.SPADES)
        as_count = 0
        for card in deck._cards:
            if card == as_card:
                as_count += 1
        self.assertEqual(as_count, 1)

    def test_new_double_deck(self):
        deck = Deck(2)
        self.assertEqual(deck.size(), 2 * _DECK_SZ)

        as_card = Card(Rank.ACE, Suit.SPADES)
        as_count = 0
        for card in deck._cards:
            if card == as_card:
                as_count += 1
        self.assertEqual(as_count, 2)

    def test_shuffle_deck(self):
        deck = Deck()
        deck.shuffle()
        card1 = Card(Rank.ACE, Suit.SPADES)
        card2 = Card(Rank.TWO, Suit.SPADES)
        card1_shuffled = deck._cards[0] is not card1
        card2_shuffled = deck._cards[1] is not card2
        # Extremely unlikely to fail, but can happen
        self.assertTrue(card1_shuffled or card2_shuffled)
