"""
Sample tests
"""


from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """Tests the `calc` module."""

    def test_add(self):
        """Test addition."""
        res: float = calc.add(5, 6)

        self.assertEqual(res, 11)

    def test_subtract(self):
        """Test subtraction."""
        res: float = calc.subtract(6, 4)

        self.assertEqual(res, 2)
