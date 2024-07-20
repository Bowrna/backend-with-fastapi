# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from random import randint
from typing import List

app = FastAPI()
origins = [
    "http://localhost:5173", 
    "http://localhost:8000", 
    "https://fuzzy-acorn-xjpjpxr5v42qwg-3000.app.github.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    
    allow_headers=["Authorization", "Content-Type", "Accept"],
    expose_headers=["*"]
)
# origins = [
#     "https://fuzzy-acorn-xjpjpxr5v42qwg-3000.app.github.dev",
#     "http://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["GET","POST"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

"""
Sample data

candy_set = {
    "id": 1,
    "candies": [
        {"id": 1, "size": 5},
        {"id": 2, "size": 5},
        {"id": 3, "size": 5},
        {"id": 4, "size": 5},
        {"id": 5, "size": 5},
        {"id": 6, "size": 5},
    ],

}
"""

candy_sets = {}

class Candy(BaseModel):
    id: int
    size: int
    color: str


class CandySet(BaseModel):
    id: int
    candies: List[Candy]


@app.get("/")
def hello_world():
    return {"message":"Hello World"}

# Get candies
@app.get("/candies/{candy_set_id}")
def get_candies(candy_set_id: int):
    global candy_sets
    candies = [Candy(id=i, size=randint(1, 10)) for i in range(6)]
    candy_set = CandySet(id=candy_set_id, candies=candies)
    candy_sets[candy_set_id] = candy_set
    return candy_set


@app.get("/{name}")
def hello_world(name: str):
    message = {"message": "Hello " + name}
    return message

# Lick candies

@app.post("/lick/{candy_set_id}")
def lick_candies(candy_set_id: int):
    global candy_sets
    if candy_set_id not in candy_sets:
        raise HTTPException(status_code=404, detail="Candy set not found")
    candy_set = candy_sets[candy_set_id]
    for candy in candy_set.candies:
        candy.size -= randint(0, 3)
        if candy.size < 0:
            candy.size = 0
    return candy_set


# Bite Candies
@app.post("/bite/{candy_set_id}")
def bite_candy(candy_set_id: int):
    """
    Bite a candy from a candy set
    """
    bite = False
    global candy_sets
    if candy_set_id not in candy_sets:
        raise HTTPException(status_code=404, detail="Candy set not found")
    candy_set = candy_sets[candy_set_id]
    for candy in candy_set.candies:
        if candy.size < 5 and candy.size > 0:
            bite = True
            candy.size -= randint(3, 5)
            if candy.size < 0:
                candy.size = 0
    if not bite:
        raise HTTPException(status_code=400, detail="No candies can be bitten")
    return candy_set