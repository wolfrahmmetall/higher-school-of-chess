from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Game(Base):
    __tablename__ = "games"

    uuid = Column(String, primary_key=True, index=True)
    white = Column(String, index=True)
    black = Column(String, index=True)
    result = Column(Integer, nullable=True)  # -1, 0, 1 или None
    moves = Column(JSON, nullable=True)  # Список ходов