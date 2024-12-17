import logging
import uuid
from fastapi import APIRouter, HTTPException, Depends
from pydantic import UUID4, BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from dbpackage.DBHelper import db_helper_game
from game.game_creation.crud import GameCreate, create_game, get_game, update_game
from api_v1.user.User import User
from api_v1.user.views import get_current_user
router = APIRouter()

class Move(BaseModel):
    start: str  # Начальная позиция, например "e2"
    end: str  # Конечная позиция, например "e4"

class GameCreateRequest(BaseModel):
    # uuid: str
    white: Optional[int] = None
    black: Optional[int] = None

class GameOut(BaseModel):
    uuid: str
    white: Optional[int] # ID игрока (int)
    black: Optional[int] # ID игрока (int)
    result: Optional[int] # Результат игры
    moves: list # Ходы игры (храним как JSON)


# @router.post("/setup/", response_model=GameOut)
@router.post("/setup/")
async def create_new_game(
    game_request: GameCreateRequest,
    db: AsyncSession = Depends(db_helper_game.scoped_session_dependency),
    current_user: User = Depends(get_current_user),  # Получаем текущего пользователя
):
    """Создает новую игру."""
    print(current_user.login, current_user.id)
    if game_request.white and game_request.black:
        raise HTTPException(status_code=400, detail="Нельзя одновременно указать обоих игроков как белого и черного.")
    
    # Устанавливаем сторону на основе запроса
    white = current_user.id if game_request.white else None
    black = current_user.id if game_request.black else None

    game = GameCreate(
        uuid=str(uuid.uuid4()),
        white=white,
        black=black,
    )
    game_data = await create_game(db=db, game=game)
    return game_data

@router.get("/{uuid}/")
async def fetch_game(uuid: str, db: AsyncSession = Depends(db_helper_game.scoped_session_dependency)):
    """Получает данные игры по UUID."""
    game = await get_game(db=db, game_uuid=uuid)
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return game

@router.put("/{uuid}/")
async def update_existing_game(uuid: str, game_request: GameCreateRequest, db: AsyncSession = Depends(db_helper_game.scoped_session_dependency)):
    """Обновляет существующую игру."""
    updated_game = await update_game(session=db, game_uuid=uuid, game_data=game_request)
    if not updated_game:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return updated_game

@router.post("/{uuid}/move/")
async def make_game_move(uuid: str, move: Move, db: AsyncSession = Depends(db_helper_game.scoped_session_dependency)):
    """Добавляет ход в существующую игру."""
    game = await get_game(db=db, game_uuid=uuid)
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")

    # Логика обновления ходов
    moves = game.moves or []
    moves.append(f"{move.start}-{move.end}")

    await update_game(session=db, game_uuid=uuid, game_data=GameCreateRequest(
        uuid=game.uuid,
        white=game.white,
        black=game.black,
        moves=moves
    ))

    return {"message": "Ход выполнен", "moves": moves}
