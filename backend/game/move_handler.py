from fastapi import APIRouter, HTTPException, Depends
from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from uuid import UUID, uuid4
from api_v1.user.views import get_current_user, get_current_user_id
from dbpackage.DBHelper import db_helper_game
from game.game_creation.crud import create_game, get_game, update_game
from game.chess_game import ChessGame

router = APIRouter()

# Хранилище активных игр
active_games: Dict[str, ChessGame] = {}

class Move(BaseModel):
    start: str  # Начальная позиция, например "e2"
    end: str  # Конечная позиция, например "e4"

class GameSetup(BaseModel):
    game_time: int  # Время на партию в минутах
    increment: int  # Инкремент в секундах
    white: bool
    black: bool


@router.post("/setup")
async def setup_game(settings: GameSetup,
               session: AsyncSession = Depends(db_helper_game.scoped_session_dependency),
               curr_user: int = Depends(get_current_user_id)):
    """
    Настраивает новую игру с указанными параметрами.
    """
    uuid = str(uuid4())
    # try:
    game = ChessGame(settings.game_time,
                         settings.increment)
        # if settings.white:
        #     game.white = curr_user
        # if settings.black:
        #     game.black = curr_user

    game.start_game()  # Инициализация игры
    active_games[uuid] = game
    await create_game(session, game)
    return {
        "message": "Игра настроена",
        "uuid": uuid,
        "game_time": settings.game_time,
        "increment": settings.increment,
    }
    # except Exception as e:
    #     print(str(e))
        # raise HTTPException(status_code=500, detail=f"Ошибка при настройке игры: {str(e)}")


@router.post("/{uuid}/move")
async def make_move(uuid: str, move: Move, 
                    session: AsyncSession = Depends(db_helper_game.scoped_session_dependency),
                    # curr_user: int = Depends(get_current_user_id)
                    ) -> Dict[str, Any]:
    """
    Обрабатывает ход в игре.
    """
    game = active_games.get(uuid)
    if game is None:
        raise HTTPException(status_code=404, detail="Игра не найдена")

    try:
        # if curr_user != game.white or curr_user != game.black:
        #     return {
        #     "board": game.board,
        #     "current_turn": game.current_player_color,
        #     "result": game.result,
        # }
        game.move(move.start, move.end)
        board_state: List[List[str]] = [
            # [piece.name() if piece else '\uA900' for piece in row]
            [piece.name() if piece else '\u00A0' for piece in row]
            for row in game.board.board
        ]
        active_games[uuid] = game
        return {
            "board": board_state,
            "current_turn": game.current_player_color,
            "result": game.result,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при обработке хода: {str(e)}")

@router.get("/{uuid}/state")
async def get_game_state(uuid: str, db: AsyncSession = Depends(db_helper_game.scoped_session_dependency)) -> Dict[str, Any]:
    """
    Возвращает текущее состояние доски и информацию об игре.
    """
    game = active_games.get(uuid)
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")

    board_state: List[List[str]] = [
        [piece.name() if piece else '\u00A0' for piece in row]
        for row in game.board.board
    ]

    return {
        "uuid": uuid,
        "board": board_state,
        "current_turn": game.current_player_color,
        "white_timer": game.white_timer,
        "black_timer": game.black_timer,
        "result": game.result,
    }

@router.delete("/{uuid}/delete")
async def delete_game(uuid: str, db: AsyncSession = Depends(db_helper_game.scoped_session_dependency)) -> Dict[str, str]:
    """
    Удаляет игру из активного списка и базы данных.
    """
    if uuid in active_games:
        del active_games[uuid]

    deleted = await delete_game(db, game_uuid=uuid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Игра не найдена")

    return {"message": "Игра удалена"}
