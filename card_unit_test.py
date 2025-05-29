import time
import unittest
from unittest.mock import patch
from card_holder import Card


class TestCard(unittest.TestCase):

    def test_init_with_empty_history(self):
        card = Card("Card 1", "Front 1", "Back 1", None)
        self.assertEqual(card.name, "Card 1")
        self.assertEqual(card.front, "Front 1")
        self.assertEqual(card.back, "Back 1")
        self.assertEqual(card.history, [])
        self.assertEqual(card.flipped, 0)
        self.assertEqual(card.passed_number, 0)
        self.assertEqual(card.last_passed_time, -1)

    def test_init_with_history(self):
        history = [{"time": 123456789, "result": "passed"}]
        card = Card("Card 2", "Front 2", "Back 2", history)
        self.assertEqual(card.name, "Card 2")
        self.assertEqual(card.front, "Front 2")
        self.assertEqual(card.back, "Back 2")
        self.assertEqual(card.history, history)
        self.assertEqual(card.flipped, 0)
        self.assertEqual(card.passed_number, 1)
        self.assertEqual(card.last_passed_time, 123456789)

    def test_flip(self):
        card = Card("Card 3", "Front 3", "Back 3", None)
        card.flip()
        self.assertEqual(card.flipped, 1)
        card.flip()
        self.assertEqual(card.flipped, 0)

    def test_show(self):
        card = Card("Card 4", "Front 4", "Back 4", None)
        self.assertEqual(card.show(), "Front 4")  # Initial state
        card.flip()
        self.assertEqual(card.show(), "Back 4")  # After flip

    def test_update_history(self):
        card = Card("Card 5", "Front 5", "Back 5", None)
        card.update_history("passed")
        self.assertEqual(len(card.history), 1)
        self.assertEqual(card.history[0]["result"],  "passed")
        self.assertAlmostEqual(card.history[0]["time"], time.time(), delta=50)


if __name__ == "__main__":
    unittest.main()
