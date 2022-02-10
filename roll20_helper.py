from fastapi import FastAPI

def make_spell_macro(base_spell_slot: int,
                     damage_per_level: str, 
                     static_damage: str = '0', 
                     max_slot: int = 9) -> str:
    """Makes a Roll20 spell macro with dropdown spell level selection.
       Note: Currently only support damage dice with no prefix (Ex. d8/level not 2d8/level)

    Args:
        base_spell_slot (int): The standard spell slot for the spell.
        damage_per_level (str): The scaling damage die per extra spell slot (ex. 'd8').
        static_damage (str, optional): Any damage that does not scale the level.
                                       (ex. '4' or 'd6+2'). Defaults to 0.
        max_slot (int, optional): The maximum spell slot that the spell can be upcast
                                  to for additional damage. Defaults to 9.

    Raises:
        Exception: [description]
        Exception: [description]
        Exception: [description]

    Returns:
        str: The formatted macro to use in the Roll20 damage slot. 
             To use in a class action, simply wrap the expression in a pair of double square brackets.
    """
    if not (1 <= base_spell_slot <= 9):
        raise Exception('Base spell slot must be between 1 and 9.')
    if not (1 <= max_slot <= 9):
        raise Exception('Max spell slot must be between 1 and 9.')
    if max_slot < base_spell_slot:
        raise Exception('Base spell cannot be greater than max spell slot.')

    static_damage_text = '' if static_damage == '0' else f'+{static_damage}'

    # Ex. ?{What Spell Slot of Smite?|None,No Smite|1,[[2d8]] Radiant Damage|2,[[3d8]] Radiant Damage|3,[[4d8]] Radiant Damage|4,[[5d8]] Radiant Damage}
    dropdown_choices = [f'{level} ({level}{damage_per_level}{static_damage_text}),{level}' for level in range(base_spell_slot, max_slot)]
    dropdown_string = '|'.join(dropdown_choices)

    # Ex. [[?{spell slot? (+d8)|1}+2]]d8
    return f'[[?{{Spell slot?|{dropdown_string}}}]]{damage_per_level}{static_damage_text}'

def main():
    print(make_spell_macro(1, 'd8', '3', 9))

if __name__ == "__main__":
    main()