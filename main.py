from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from roll20_helper import SpellMacroGenerator

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://roll20-helper.herokuapp.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/spell_macro")
def read_spell_macro(base_spell_slot: int,
                     damage_per_level: str, 
                     static_damage: Optional[str] = '0', 
                     max_slot: Optional[int] = 9):
    try:
        damage_macro = SpellMacroGenerator.damage_macro(base_spell_slot, static_damage, damage_per_level, max_slot)
    except:
        # TODO: Real excpetion handling.
        damage_macro = 'Unable to create macro, please check values.'
        signature = make_signature(base_spell_slot=base_spell_slot, static_damage=static_damage, damage_per_level=damage_per_level, max_slot=max_slot)
        print(f'Failed to parse: {signature}')
    
    return {'macro' : damage_macro}

def make_signature(**kwargs):
    return [f'{name} = {value}' for name, value in kwargs.items()]