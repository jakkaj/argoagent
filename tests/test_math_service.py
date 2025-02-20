import unittest
from tools.calc.math_service import parse_and_solve


class TestMathService(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(parse_and_solve("2+2"), "4")

    def test_division(self):
        self.assertEqual(parse_and_solve("10/2"), "5.0")

    def test_multiplication(self):
        self.assertEqual(parse_and_solve("3*3"), "9")

    def test_invalid_expression(self):
        result = parse_and_solve("invalid")
        self.assertTrue(result.startswith("Error:"))


if __name__ == '__main__':
    unittest.main()
