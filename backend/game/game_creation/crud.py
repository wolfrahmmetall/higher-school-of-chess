from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from typing import Optional, List
from uuid import uuid4
from game.chess_game import ChessGame
from game.game_creation.Game import Games

async def create_game(db: AsyncSession, game: ChessGame, uuid: str) -> Games:
    """
    Создает новую игру в базе данных.
    """
    db_game = Games(
        uuid=uuid,
        white=game.white,
        black=game.black,
        result=game.result,
        board={'board': game.board.pretty_board()},
        game_time=game.white_timer,
        increment=game.increment,
        # white_timer=game.game_time,
        # black_timer=game.game_time,
        current_player_color="white",
        is_active=True
    )
    db.add(db_game)
    await db.commit()
    await db.refresh(db_game)
    return db_game

async def get_game(db: AsyncSession, game_uuid: str) -> Optional[Games]:
    """
    Возвращает игру по UUID из базы данных.
    """
    query = select(Games).where(Games.uuid == game_uuid)
    result = await db.execute(query)
    try:
        return result.scalar_one()
    except NoResultFound:
        return None

async def update_game(db: AsyncSession, game_uuid: str, updated_data: dict) -> Optional[Games]:
    """
    Обновляет данные существующей игры.
    """
    game = await get_game(db, game_uuid)
    if not game:
        return None

    for key, value in updated_data.items():
        if hasattr(game, key):
            setattr(game, key, value)

    await db.commit()
    await db.refresh(game)
    return game

async def get_all_games(db: AsyncSession) -> List[Games]:
    """
    Возвращает список всех игр в базе данных.
    """
    query = select(Games)
    result = await db.execute(query)
    return result.scalars().all()

async def delete_game(db: AsyncSession, game_uuid: str) -> bool:
    """
    Удаляет игру из базы данных по UUID.
    """
    game = await get_game(db, game_uuid)
    if not game:
        return False

    await db.delete(game)
    await db.commit()
    return True
