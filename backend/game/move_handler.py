from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json

# Импорт предоставленных файлов
from game.board import Board
from game.chess_game import ChessGame

# Создание роутера
router = APIRouter()
# Глобальный объект игры

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


@router.post("/setup")
def setup_game(settings: GameSetup):
    """
    Настраивает новую игру с указанными параметрами.
    """
    global game
    game = ChessGame(game_time=settings.game_time, increment=settings.increment)
    return {
        "message": "Игра настроена",
        "game_time": settings.game_time,
        "increment": settings.increment,
    }


@router.get("/state")
def get_game_state() -> Dict[str, Any]:
    """
    Возвращает текущее состояние доски и информации об игре.
    """
    if game is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Игра ещё не настроена")
    
    board_state = [[piece.name if piece else None for piece in row] for row in game.board.board]
    return {
        "board": board_state,
        "current_turn": game.current_player_color,
    }


@router.post("/move")
def make_move(move: Move):
    """
    Выполняет ход в игре.
    """
    if game is None:
        raise HTTPException(status_code=403, detail="Игра ещё не настроена")
    
    try:
        result = game.move(move.start, move.end)
        return {
            "board": [[piece.name if piece else None for piece in row] for row in game.board.board],
            "current_turn": game.current_player_color,
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/restart")
def restart_game():
    """
    Перезапускает игру с теми же параметрами.
    """
    global game
    if game is None:
        raise HTTPException(status_code=400, detail="Игра ещё не настроена")
    
    game = ChessGame(game_time=game.game_time, increment=game.increment)
    return {
        "message": "Игра перезапущена",
        "board": [[piece.name if piece else None for piece in row] for row in game.board],
        "current_turn": game.current_turn,
        "status": game.status,
    }
