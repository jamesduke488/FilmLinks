import pandas as pd
import numpy as np
import requests
import os
from fastapi import HTTPException, FastAPI

def check_omdb_key(api_key: str) -> None:
    r = requests.get(
        "https://www.omdbapi.com/",
        params={"apikey": api_key, "s": "Inception", "plot": "short"},
        timeout=5
    )
    data = r.json()
    if data.get("Response") != "True":
        raise RuntimeError(f"OMDb API error: {data.get('Error')}")
    else:
        print("Key working fine")
        if data.get("Response") == "True":
            print(data.get("totalResults"))
            for film in data.get("Search"):

                for key, value in film.items():
                    print(f"{key}: {value}")

                print()
        else:
            print("No films loser")

MY_DIRECTORY = 'C:\\Users\\James Duke\\'
OMDB_URL = "https://www.omdbapi.com/"

with open(os.path.join(MY_DIRECTORY, '.secret', 'file.txt')) as f:
    API_KEY = f.read()

check_omdb_key(API_KEY)

title = 'Inception'
params = {"t": title, "apikey": API_KEY, "plot": "short"}

try:
    req = requests.get(OMDB_URL, params=params, timeout=8)
    
except requests.RequestException as e:
    print(e)
    raise HTTPException(status_code=502, detail="Upstream error")
if req.status_code != 200:
    print(req.status_code)
    raise HTTPException(status_code=502, detail="Upstream error")

data = req.json()
if data.get("Response") != "True":
        raise HTTPException(status_code=404, detail=data.get("Error", "Not found"))
res = {
    "title": data.get("Title"),
    "year": data.get("Year"),
    "director": data.get("Director"),
    "rating": next((x["Value"] for x in data.get("Ratings", []) if x["Source"]=="Internet Movie Database"), None),
    "genre": data.get("Genre"),
    "plot": data.get("Plot"),
}

for key, value in res.items():
    print(f"{key}: {value}")

from pydantic import BaseModel

class FilmItem(BaseModel):
    title: str
    director: str
    plot: str | None = None

app = FastAPI()


items_db = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: FilmItem):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    items_db.append(item_dict)

@app.get("/items/")
async def get_items():
    return items_db