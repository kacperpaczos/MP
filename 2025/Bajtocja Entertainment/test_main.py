import unittest
from main import znajdz_podzial

class TestRozwiazanie(unittest.TestCase):
    def test_przyklad_1(self):
        """Test dla pierwszego przykładu z zadania"""
        n = 7
        arr = [3, 1, 2, 6, 1, 4, 1]
        wynik = znajdz_podzial(n, arr)
        self.assertIsNotNone(wynik)
        self.assertEqual(len(wynik), 3)
        self.assertEqual(wynik, [3, 4, 7])

    def test_przyklad_2(self):
        """Test dla drugiego przykładu z zadania"""
        n = 4
        arr = [2, 0, 2, 5]
        wynik = znajdz_podzial(n, arr)
        self.assertIsNone(wynik)

    def test_przyklad_3(self):
        """Test dla trzeciego przykładu z zadania"""
        n = 6
        arr = [3, 3, 3, 3, 3, 3]
        wynik = znajdz_podzial(n, arr)
        self.assertIsNotNone(wynik)
        self.assertTrue(2 <= len(wynik) <= n)
        self.assertEqual(wynik[-1], n)

    def test_przyklad_4(self):
        """Test dla czwartego przykładu z zadania"""
        n = 4
        arr = [-3, 1, 1, -1]
        wynik = znajdz_podzial(n, arr)
        self.assertIsNotNone(wynik)
        self.assertEqual(len(wynik), 2)
        self.assertEqual(wynik, [3, 4])

if __name__ == "__main__":
    unittest.main() 