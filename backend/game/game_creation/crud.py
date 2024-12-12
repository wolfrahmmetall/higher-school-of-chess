# backend/game/crud.py
from sqlalchemy.orm import Session
from ..game_creation import Game
from pydantic import BaseModel
from typing import List, Optional

class GameCreate(BaseModel):
    uuid: str
    white: int # id игрока в БД -- инт
    black: int # id игрока в БД -- инт
    result: Optional[int] = None
    moves: List[str] = []

def create_game(db: Session, game: GameCreate):
    db_game = Game(
        uuid=game.uuid,
        white=game.white, # id игрока
        black=game.black, # id игрока
        result=game.result,
        moves=game.moves
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def get_game(db: Session, game_uuid: str):
    return db.query(Game).filter(Game.uuid == game_uuid).first()

def get_games(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Game).offset(skip).limit(limit).all()

def update_game(db: Session, game_uuid: str, game_data: GameCreate):
    db_game = db.query(Game).filter(Game.uuid == game_uuid).first()
    if db_game:
        db_game.white = game_data.white
        db_game.black = game_data.black
        db_game.result = game_data.result
        db_game.moves = game_data.moves
        db.commit()
        db.refresh(db_game)
    return db_game

def delete_game(db: Session, game_uuid: str):
    db_game = db.query(Game).filter(Game.uuid == game_uuid).first()
    if db_game:
        db.delete(db_game)
        db.commit()
    return db_game