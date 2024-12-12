from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from fastapi.responses import JSONResponse
from uuid import uuid4

from sqlalchemy.orm import Session
from dbpackage.session import SessionLocal
from .game import Game

from .pieces.piece import Piece

# Импорт предоставленных файлов
from .board import Board
from .chess_game import ChessGame

# Создание роутера
router = APIRouter()

# Глобальный объект игры
game: Optional[ChessGame] = None

# Pydantic модель для настройки игры
class GameSetup(BaseModel):
    game_time: int  # Время на партию в минутах
    increment: int  # Инкремент в секундах

# Pydantic модель для хода
class Move(BaseModel):
    start: str  # Начальная позиция, например "e2"
    end: str  # Конечная позиция, например "e4"
    
class NewGame(BaseModel):
    uuid: str
    white: str
    black: str
    result: Optional[int] = None
    moves: List[str] = []

# надо сделать жесточайшую поправку на то, что нам надо поддерживать кучу инстансов игр
@router.post("/games")
async def create_game(new_game: NewGame):
    """
    Создает новую игру в базе данных.
    """
    async with SessionLocal() as db:  # Используем асинхронный контекст
        try:
            game = Game(
                uuid=new_game.uuid,
                white=new_game.white,
                black=new_game.black,
                result=new_game.result,
                moves=new_game.moves
            )
            db.add(game)  # Добавление игры в сессию
            await db.commit()  # Сохранение изменений
            await db.refresh(game)  # Обновление объекта игры
            return {"message": "Игра успешно создана", "game": game}
        except Exception as e:
            await db.rollback()  # Откат изменений в случае ошибки
            raise HTTPException(status_code=500, detail=f"Ошибка при создании игры: {str(e)}")

# после этого игра должна создаваться
@router.post("/setup")
def setup_game(settings: GameSetup):
    """
    Настраивает новую игру с указанными параметрами.
    """
    global game
    try:
        game = ChessGame(game_time=settings.game_time, increment=settings.increment)
        game.start_game()  # Инициализация игры
        return {
            "message": "Игра настроена",
            "game_time": settings.game_time,
            "increment": settings.increment,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при настройке игры: {str(e)}")


# игра должна быть получена по game_id: uuid
# @router.get("/{user_id}/state")
# def get_game_state(user_id: str) -> Dict[str, Any]:
# и все функции надо переписать на такие адреса
@router.get("/state")
def get_game_state() -> Dict[str, Any]:
    """
    Возвращает текущее состояние доски и информации об игре.
    """
    if game is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Игра ещё не настроена")

    try:
        board_state: List[List[str]] = [
            # [piece.name() if piece else '\uA900' for piece in row]
            [piece.name() if piece else '\u00A0' for piece in row]
            for row in game.board.board
        ]
        return {
            "board": board_state,
            "current_turn": game.current_player_color,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении состояния игры: {str(e)}")

@router.post("/move")
def make_move(move: Move):
    """
    Выполняет ход в игре.
    """
    if game is None:
        raise HTTPException(status_code=403, detail="Игра ещё не настроена")

    try:
        result = game.move(move.start, move.end)
        board_state: List[List[str]] = [
            # [piece.name() if piece else '\uA900' for piece in row]
            [piece.name() if piece else '\u00A0' for piece in row]
            for row in game.board.board
        ]
        return {
            "board": board_state,
            "current_turn": game.current_player_color,
            "result": game.result,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при выполнении хода: {str(e)}")

@router.post("/restart")
def restart_game():
    """
    Перезапускает игру с теми же параметрами.
    """
    global game
    if game is None:
        raise HTTPException(status_code=400, detail="Игра ещё не настроена")

    try:
        game = ChessGame(game_time=game.game_time, increment=game.increment)
        game.start_game()
        board_state: List[List[str]] = [
            # [piece.name() if piece else '\uA900' for piece in row]
            [piece.name() if piece else '\u00A0' for piece in row]
            for row in game.board.board
        ]
        return {
            "message": "Игра перезапущена",
            "board": board_state,
            "current_turn": game.current_player_color,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при перезапуске игры: {str(e)}")
