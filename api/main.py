from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from api.models import Film
from api.setup_db import SessionLocal, engine, Base
from api.schema import FilmCreate, FilmReturn

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/films/", response_model=List[FilmReturn])
def get_all_films(db: Session = Depends(get_db)):
    return db.query(Film).all()

@app.post("/films/add", response_model=FilmReturn)
def add_new_film(film: FilmCreate, db: Session = Depends(get_db)):
    new_film = Film(
        title = film.title,
        director = film.director,
        release_year = film.release_year,
        genre = film.genre,
        rating = film.rating  # e.g. PG, 12A, R
    )
    db.add(new_film)
    db.commit()
    db.refresh(new_film)
    return new_film


@app.get("/films/{film_id}", response_model=FilmReturn)
def get_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.film_id == film_id).first()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film

@app.get("/films/search/")
def search(title: str, db: Session = Depends(get_db)):
    return db.query(Film).filter(Film.title.ilike(f"%{title}%")).all()