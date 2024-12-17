# backend/game/views.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dbpackage.session import SessionLocal_game
from .crud import create_game, get_game, get_games, update_game, delete_game
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix='/game')

# Pydantic модель для новой игры
class NewGame(BaseModel):
    uuid: str
    white: str
    black: str
    result: Optional[int] = None
    moves: List[str] = []

# а зачем это нам? мы же игру создаем через game/setup, оттуда пробиваем create_game по uuid и инстанс игры передаем в move_handler
@router.post("/create") 
async def create_game_endpoint(new_game: NewGame, db: Session = Depends(SessionLocal_game)):
    """
    Создает новую игру в базе данных.
    """
    game = create_game(db, new_game)
    return {"message": "Игра успешно создана", "game": game}
