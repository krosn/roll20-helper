from re import M
import unittest
from roll20_helper import SpellMacroGenerator

class TestSpellMacroGenerator(unittest.TestCase):
    default_base_level = 1
    default_scaling_damage = '3d8'
    default_base_damage = 'd6'
    default_max_level = 9

    def test_damage_macro_success(self):
        with self.subTest('Level 1 spell with d8/level and d3 base damage scaled levels 1-9'):
            actual_text = SpellMacroGenerator.damage_macro(base_spell_slot=1, base_damage='3', damage_per_level='d8')
            expected_text = '[[?{What spell slot?|Level 1 (3),0|Level 2 (3 + 1d8),1|Level 3 (3 + 2d8),2|Level 4 (3 + 3d8),3|Level 5 (3 + 4d8),4|Level 6 (3 + 5d8),5|Level 7 (3 + 6d8),6|Level 8 (3 + 7d8),7|Level 9 (3 + 8d8),8}]]d8 + 3'
            self.assertEqual(expected_text, actual_text)
        
        with self.subTest('Level 5 spell with 2d6/level and 3d8 base damage scaled levels 5-8'):
            actual_text = SpellMacroGenerator.damage_macro(base_spell_slot=5, base_damage='3d8', damage_per_level='2d6', max_slot=8)
            expected_text = '[[?{What spell slot?|Level 5 (3d8),0|Level 6 (3d8 + 2d6),2|Level 7 (3d8 + 4d6),4|Level 8 (3d8 + 6d6),6}]]d6 + 3d8'
            self.assertEqual(expected_text, actual_text)

    def test_damage_macro_base_level(self):
        for base_level in range (-2, 15):
            if 1 <= base_level <= 8:
                with self.subTest(f'Spell with base level {base_level} should be valid'):
                    _ = SpellMacroGenerator.damage_macro(base_spell_slot=base_level, 
                                                         base_damage=self.default_base_damage, 
                                                         damage_per_level=self.default_scaling_damage, 
                                                         max_slot=self.default_max_level)
            else:
                with self.subTest(f'Spell with base level {base_level} should raise exception'):
                    with self.assertRaises(Exception):
                        _ = SpellMacroGenerator.damage_macro(base_spell_slot=base_level, 
                                                             base_damage=self.default_base_damage, 
                                                             damage_per_level=self.default_scaling_damage, 
                                                             max_slot=self.default_max_level)

    def test_damage_macro_max_level(self):
        for max_level in range (-2, 15):
            if 1 <= max_level <= 9:
                with self.subTest(f'Spell with max level {max_level} should be valid'):
                    _ = SpellMacroGenerator.damage_macro(base_spell_slot=self.default_base_level, 
                                                         base_damage=self.default_base_damage, 
                                                         damage_per_level=self.default_scaling_damage, 
                                                         max_slot=max_level)
            else:
                with self.subTest(f'Spell with max level {max_level} should raise exception'):
                    with self.assertRaises(Exception):
                        _ = SpellMacroGenerator.damage_macro(base_spell_slot=self.default_base_level, 
                                                             base_damage=self.default_base_damage, 
                                                             damage_per_level=self.default_scaling_damage, 
                                                             max_slot=max_level)
    
    def test_damage_macro_base_level_greater_than_or_max_level(self):
        base_level = 5
        max_level = 4

        with self.assertRaises(Exception):
            _ = SpellMacroGenerator.damage_macro(base_spell_slot=base_level, 
                                                 base_damage=self.default_base_damage, 
                                                 damage_per_level=self.default_scaling_damage, 
                                                 max_slot=max_level)
    