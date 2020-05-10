import pytest
from pyarcade.games.card import Rank, Suit, Card
from pyarcade.games.deck import Deck
from pyarcade.games.player import Player
from pyarcade.games.crazy_eights import CrazyEights
import unittest


@pytest.mark.local
class CrazyEightsTestCase(unittest.TestCase):
    def test_setup_round(self):
        pass

    def test_setup_game(self):
        pass

    def test_deal(self):
        game = CrazyEights(4)
        p1 = game.players.get(1)
        self.assertEqual(len(p1.get_cards()), 5)

        game.deal(5)
        self.assertEqual(len(p1.get_cards()), 10)

    def test_draw(self):
        game = CrazyEights(2)
        game.draw(1)
        self.assertEqual(len(game.players.get(1).get_cards()), 8)

    def test_play(self):
        game = CrazyEights(4)
        tc = Card(Rank.KING, Suit.HEARTS)
        game.discard.append(tc)
        p1 = game.players.get(1)
        p2 = game.players.get(2)

        # Card cannot be played
        card = Card(Rank.TWO, Suit.CLUBS)
        p1.add_to_hand(card)
        self.assertFalse(game.play(1, card))
        self.assertEqual(len(p1.get_cards()), 6)
        self.assertEqual(game.discard[-1], tc)

        # Card matches rank
        card = Card(Rank.KING, Suit.SPADES)
        p1.add_to_hand(card)
        game.play(1, card, Suit.DIAMONDS)
        self.assertEqual(len(p1.get_cards()), 6)
        self.assertEqual(game.discard[-1], card)

        # Card is an eight, matches neither rank nor suit
        card = Card(Rank.EIGHT, Suit.CLUBS)
        p2.add_to_hand(card)
        game.play(2, card, Suit.DIAMONDS)
        self.assertEqual(len(p2.get_cards()), 5)
        self.assertEqual(game.discard[-1], card)
        self.assertEqual(game.curr_suit, Suit.DIAMONDS)

    def test_playable(self):
        game = CrazyEights(4)
        card = Card(Rank.NINE, Suit.HEARTS)
        game.discard.append(card)
        self.assertFalse(game.playable(Card(Rank.ACE, Suit.SPADES)))
        self.assertTrue(game.playable(Card(Rank.NINE, Suit.SPADES)))
        self.assertTrue(game.playable(Card(Rank.ACE, Suit.HEARTS)))
        self.assertTrue(game.playable(Card(Rank.EIGHT, Suit.SPADES)))

    def test_get_top_card_suit(self):
        game = CrazyEights(4)
        game.discard.append(Card(Rank.ACE, Suit.SPADES))
        self.assertEqual(game.get_top_card_suit(), Suit.SPADES)
        game.discard.append(Card(Rank.EIGHT, Suit.SPADES))
        game.curr_suit = Suit.HEARTS
        self.assertEqual(game.get_top_card_suit(), Suit.HEARTS)

    def test_play_options(self):
        game = CrazyEights(4)
        p1 = game.players.get(1)

        p1.clear_hand()
        cards = [Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS),
                 Card(Rank.JACK, Suit.SPADES)]
        [p1.add_to_hand(card) for card in cards]

        game.discard.append(Card(Rank.TEN, Suit.SPADES))
        card_ops = game.play_options(1)
        self.assertEqual(len(card_ops), 2)
        self.assertTrue(all(card in p1.get_cards() for card in card_ops))

    def test_turn(self):
        game = CrazyEights(4)
        [p.clear_hand() for p in game.players.values()]  # force players to draw

        game.turn(2)
        game.turn(3)
        game.turn(4)

    def test_reset_round(self):
        game = CrazyEights(2)
        p1 = game.players.get(1)
        p2 = game.players.get(2)
        p1.clear_hand()
        p2.clear_hand()
        p1.add_to_hand(Card(Rank.ACE, Suit.CLUBS))
        p2.add_to_hand(Card(Rank.EIGHT, Suit.DIAMONDS))
        game.reset_round()
        self.assertEqual(p1.get_score(), 49)

    def test_reset(self):
        game = CrazyEights(4)
        game.reset()

        score_hist = False
        if game.game_hist:
            for p in game.game_hist[0][0].values():
                if p.get_score() > 0:
                    score_exists = True
                    break
        self.assertTrue(score_exists)

    def test_clear(self):
        game = CrazyEights(4)
        game.reset()  # force starting hands to be scored and stored
        game.clear()

        for p in game.players.values():
            self.assertEqual(p.get_score(), 0)
        self.assertEqual(len(set(game.pts)), 1)

    def test_stress1(self):
        """Create a new game with two players and play out several rounds.
        """
        pass

    def test_stress2(self):
        """Create a new game with seven players and play out multiple games.
        """
        pass
