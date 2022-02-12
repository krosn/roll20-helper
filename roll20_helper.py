from typing import Iterator, List, Tuple
import re

class Die:
    sides: int
    multiplier: int = 1

    def __init__(self, sides: int, multiplier: int) -> None:
        self.sides = int(sides)
        self.multiplier = int(multiplier)

    def multiply(self, factor: int) -> 'Die':
        return Die(self.sides, self.multiplier*factor)

    def is_die(input_string: str) -> bool:
        return re.fullmatch(r'\d*[d|D]\d+', input_string)

    def from_string(input_string: str) -> 'Die':
        input_string = input_string.lower()

        # If no number is present before the die, assume it's a single die.
        if input_string.startswith('d'):
            input_string = '1' + input_string

        tokens = input_string.split('d')

        if len(tokens) != 2:
            raise Exception(f'Failed to parse "{input_string}" as a die.')

        return Die(multiplier=tokens[0], sides=tokens[1])

    def __str__(self) -> str:
        return f'{self.multiplier}d{self.sides}'


class SpellMacroGenerator:
    @staticmethod
    def damage_macro(base_spell_slot: int,
                     base_damage: str, 
                     damage_per_level: str, 
                     max_slot: int = 9) -> str:
        # Sanity checks
        if not (1 <= base_spell_slot <= 8):
            raise Exception('Base spell slot must be between 1 and 8.')
        if not (1 <= max_slot <= 9):
            raise Exception('Max spell slot must be between 1 and 9.')
        if max_slot < base_spell_slot:
            raise Exception('Base spell cannot be greater than max spell slot.')

        # Omit the base damage if it's empty or zero.
        if not base_damage or base_damage.strip() == '0':
            base_damage = ''

        # Take the first die, ignore everything else for now.
        # TODO: Support spells that scale by a fixed amount (ex. +5/level instead of additional d4 per level)
        per_level_dice, _ = SpellMacroGenerator._separate_dice_and_integers(damage_per_level)
        per_level_die = per_level_dice[0]

        # Generate the dropdown portion. This will also determine the die multiplier.
        dropdown_choices = SpellMacroGenerator._dropdown_choices(base_spell_slot, max_slot, per_level_die, base_damage)
        dropdown_string = '|'.join(dropdown_choices)

        # Format the final macro.
        base_damage_text = f' + {base_damage}' if base_damage else ''
        return f'[[?{{What spell slot?|{dropdown_string}}}]]d{per_level_die.sides}{base_damage_text}'

    @staticmethod
    def _dropdown_choices(base_spell_slot: int,
                          max_slot: int,
                          increase_per_level: Die,
                          base_damage: str | None) -> Iterator[str]:
        for level in range(base_spell_slot, max_slot + 1):
            upcast_factor = level - base_spell_slot

            if upcast_factor == 0:
                # Avoid having a die with 0 as the multiplier. (ex. 0d6)
                multiplier = 0
                damage_die = ''
            else:
                upcast_dice = increase_per_level.multiply(upcast_factor)
                multiplier = upcast_dice.multiplier
                damage_die = str(upcast_dice)

            # Only show components with values.
            damage = f'{damage_die} + {base_damage}' if damage_die and base_damage else damage_die + base_damage

            yield f'Level {level} ({damage}),{multiplier}'

    @staticmethod
    def _separate_dice_and_integers(string: str) -> Tuple[List[Die], int]:
        dice = []
        flat_amount = 0
        
        tokens = re.split(r'[\s+]', string)

        for token in tokens:
            if not token:
                continue
            if token.isdigit():
                flat_amount += int(token)
            elif Die.is_die(token):
                dice.append(Die.from_string(token))
            else:
                raise Exception(f'Cannot parse "{string}" to dice and integers')

        return dice, flat_amount


def main():
    die = Die(sides=6, multiplier=3)
    print(f'Die: {die}')
    print()
    print(f'Multiplied by 2: {die.multiply(2)}')
    print()
    print(SpellMacroGenerator.damage_macro(1, base_damage='3', damage_per_level='d8'))
    print()
    print(SpellMacroGenerator.damage_macro(5, base_damage='3d8', damage_per_level='2d6', max_slot=8))

if __name__ == "__main__":
    main()