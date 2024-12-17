import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy import select

from .Game import Games
from pydantic import UUID4, BaseModel

class GameCreate(BaseModel):
    uuid: str
    white: Optional[int] = None  # ID игрока в БД
    black: Optional[int] = None  # ID игрока в БД
    result: Optional[int] = 0
    moves: List[str] = []

async def create_game(db: AsyncSession, game: GameCreate) -> Games:
    """Создает новую игру в базе данных."""
    db_game = Games(**game.model_dump(exclude={"id"}))
    db.add(db_game)
    await db.commit()
    await db.refresh(db_game)
    return db_game.uuid

async def get_game(db: AsyncSession, game_uuid: str):
    """Возвращает игру по её UUID."""
    return await db.get(Games, game_uuid)

async def update_game(session: AsyncSession, game_uuid: str, game_data: GameCreate):
    """Обновляет данные игры по UUID."""
    query = select(Games).where(Games.uuid == game_uuid)
    result = await session.execute(query)
    db_game = result.scalar_one_or_none()
    if db_game is None:
        return HTTPException(status_code=404, detail='Игры не существует.')
    if db_game:
        db_game.white = game_data.white
        db_game.black = game_data.black
        db_game.result = game_data.result
        db_game.moves = game_data.moves
        await session.commit()
        await session.refresh(db_game)
    return db_game

async def delete_game(db: AsyncSession, game_uuid: str):
    """Удаляет игру из базы данных по UUID."""
    db_game = db.query(Games).filter(Games.uuid == game_uuid).first()
    if db_game:
        db.delete(db_game)
        await db.commit()
    return db_game
