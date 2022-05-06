import unittest
from roll20_helper import Die

class TestDie(unittest.TestCase):
    valid_dice_input = ['d1', 'd6', 'D8', '2d6', '1000D1000']
    invalid_dice_input = ['d', '3 d6', '5d', 'd 2', 'd_5', 'd4d' '4d4d4', None, '', ' ', 'not a die']

    def test_isDie_valid(self):
        for valid_die in self.valid_dice_input:
            with self.subTest(f'[{valid_die}] should be a die'):
                self.assertTrue(Die.is_die(valid_die))

    def test_isDie_invalid(self):
        for invalid_die in self.invalid_dice_input:
            with self.subTest(f'[{invalid_die}] should NOT be a die'):
                self.assertFalse(Die.is_die(invalid_die))
            
        with self.subTest('Non-string input should raise type-error'):
            with self.assertRaises(TypeError):
                Die.is_die(4)

    def test_from_string(self):
        input_strings = ['d6', 'D8', '4d4', '10D10']
        expected_dice = [
            Die(sides=6, multiplier=1), 
            Die(sides=8, multiplier=1), 
            Die(sides=4, multiplier=4), 
            Die(sides=10, multiplier=10)
        ]

        for (input_string, expected_die) in zip(input_strings, expected_dice):
            with self.subTest(f'[{input_string}] should have ' +
                              f'a multiplier of {expected_die.multiplier} ' +
                              f'and {expected_die.sides} sides'):
                actual_die = Die.from_string(input_string)
                self.assertEqual(expected_die.multiplier, actual_die.multiplier)
                self.assertEqual(expected_die.sides, actual_die.sides)

    def test_from_string_exception(self):
        for invalid_die_input in self.invalid_dice_input:
            with self.subTest(f'[{invalid_die_input}] should throw an exception'):
                with self.assertRaises(Exception):
                    _ = Die.from_string(invalid_die_input)

    def test_multiply(self):
        die = Die(sides=3, multiplier=4)

        for i in range(-10, 11):
            with self.subTest(f'Multiplication by {i} should scale die'):
                scaled_die = die.multiply(i)
                self.assertEqual(die.multiplier * i, scaled_die.multiplier)

if __name__ == '__main__':
    unittest.main()
