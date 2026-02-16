from sqlalchemy import Column, Integer, String
from api.setup_db import Base

class Film(Base):
    __tablename__ = "films"
    film_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    director = Column(String(100), nullable=False)
    release_year = Column(Integer, nullable=False)
    genre = Column(String(50), nullable=True)
    rating = Column(String(10), nullable=True)  # e.g. PG, 12A, R


