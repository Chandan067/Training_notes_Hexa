import unittest
from unittest.mock import patch
from movie_booking import calculate_amount, book_movie

class TestBookingSystem(unittest.TestCase):

    def setUp(self):
        print("\nSetting up test case...")

    def tearDown(self):
        print("Cleaning up after test.")

    def test_calculate_amount(self):
        result = calculate_amount("Pushpa", 3)
        self.assertEqual(result, 450)

    @patch("builtins.input", side_effect=["2", "2"])
    def test_book_movie(self, mock_input):
        movie, total = book_movie()
        self.assertEqual(movie, "Dangal")
        self.assertEqual(total, 360)

if __name__ == "__main__":
    unittest.main()
