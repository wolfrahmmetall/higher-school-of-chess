from hmac import new
from fastapi import APIRouter, HTTPException, Depends
from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from uuid import UUID, uuid4
from api_v1.user.views import get_current_user_id
from api_v1.user.crud import get_user_by_id
from dbpackage.DBHelper import db_helper_game, db_helper_user
from game.game_creation.crud import create_game, get_all_games, get_game, update_game
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
    if settings.white:
        game.white = curr_user
    if settings.black:
        game.black = curr_user

    game.start_game()  # Инициализация игры
    active_games[uuid] = game
    await create_game(session, game, uuid)
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
                    curr_user: int = Depends(get_current_user_id)
                    ) -> Dict[str, Any]:
    """
    Обрабатывает ход в игре.
    """
    game = active_games.get(uuid)
    if game is None:
        raise HTTPException(status_code=404, detail="Игра не найдена")

    try:
        if curr_user != game.white and curr_user != game.black or \
            curr_user != game.white and game.current_player_color == "white" or \
                curr_user != game.black and game.current_player_color == "black":
            return {
            "message":f"Вам сейчас нельзя ходить!, ваш id: {curr_user}, белые: {game.white}, черные:",
            "board": game.board.pretty_board(),
            "current_turn": game.current_player_color,
            "result": game.result,
        }
        game.move(move.start, move.end)
        board_state: List[List[str]] = [
            # [piece.name() if piece else '\uA900' for piece in row]
            [piece.name() if piece else '\u00A0' for piece in row]
            for row in game.board.board
        ]
        active_games[uuid] = game
        return {
            "message": "Ход выполнен успешно!",
            "board": board_state,
            "current_turn": game.current_player_color,
            "result": game.result,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при обработке хода: {str(e)}")

@router.get("/{uuid}/")
async def get_game_state(uuid: str) -> Dict[str, Any]:
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

@router.post("/{uuid}/connect")
async def connect_to_game(uuid: str, session: AsyncSession = Depends(db_helper_game.scoped_session_dependency),
                          new_player: int = Depends(get_current_user_id)):
    game = active_games[uuid]   

    if game.white is None:
        game.white = new_player
        await update_game(session, uuid, {"white": game.white})

    if game.black is None:
        game.black = new_player
        await update_game(session, uuid, {"black": game.black})

    active_games[uuid] = game

    return {
        "uuid": uuid,
        "board": game.board.pretty_board(),
        "current_turn": game.current_player_color,
        "white_timer": game.white_timer,
        "black_timer": game.black_timer,
        "result": game.result,
    }

@router.get("/active-games")
async def get_active_games(db: AsyncSession = Depends(db_helper_game.scoped_session_dependency)) -> List[Dict[str, Any]]:
    """
    Возвращает список всех активных игр.
    """
    games = await get_all_games(db)
    return [
        {
            "uuid": game.uuid,
            "white": game.white,
            "black": game.black,
            "game_time": game.game_time,
            "increment": game.increment,
            "is_active": game.is_active,
            "current_turn": game.current_player_color,
        }
        for game in games if game.is_active
    ]

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

@router.get("/{uuid}/white-player")
async def get_white_player(
    uuid: str,
    session: AsyncSession = Depends(db_helper_user.scoped_session_dependency),
) -> Dict[str, Any]:
    """
    Возвращает информацию о белом игроке (логин).
    """
    game = active_games.get(uuid)
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")

    if game.white is None:
        return {"uuid": uuid, "white_player": None}

    # Получаем логин белого игрока
    white_player = await get_user_by_id(session, game.white)
    if not white_player:
        raise HTTPException(status_code=404, detail="Белый игрок не найден")

    return {
        "uuid": uuid,
        "white_player": {"login": white_player.login, "elo": white_player.elo_score},
    }


@router.get("/{uuid}/black-player")
async def get_black_player(
    uuid: str,
    session: AsyncSession = Depends(db_helper_user.scoped_session_dependency),

) -> Dict[str, Any]:
    """
    Возвращает информацию о черном игроке (логин).
    """
    game = active_games.get(uuid)
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")

    if game.black is None:
        return {"uuid": uuid, "black_player": None}

    # Получаем логин черного игрока
    black_player = await get_user_by_id(session, game.black)
    if not black_player:
        raise HTTPException(status_code=404, detail="Черный игрок не найден")

    return {
        "uuid": uuid,
        "black_player": {"login": black_player.login, "elo": black_player.elo_score},
    }
