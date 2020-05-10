import pytest
from pyarcade.games.ordered_enum import OrderedEnum
from enum import unique
import unittest


@pytest.mark.local
@unique
class Grade(OrderedEnum):
    """https://docs.python.org/3/library/enum.html#orderedenum
    """
    A = 5
    B = 4
    C = 3
    D = 2
    F = 1


class OrderedEnumTestCase(unittest.TestCase):
    def test_ordered_enum(self):
        self.assertEqual(Grade.F, Grade.F)
        self.assertGreater(Grade.A, Grade.B)
        self.assertGreaterEqual(Grade.B, Grade.C)
        self.assertLess(Grade.C, Grade.B)
        self.assertLessEqual(Grade.D, Grade.D)
