from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from roll20_helper import make_spell_macro

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
    return {'macro' : make_spell_macro(base_spell_slot, damage_per_level, static_damage, max_slot)}