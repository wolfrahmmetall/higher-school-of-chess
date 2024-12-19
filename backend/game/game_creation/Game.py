from typing import Optional, List
from uuid import uuid4
from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.sqlite import JSON
from dbpackage.Base import Base

class Games(Base):
    """
    Таблица для хранения данных об играх.
    """
    # Уникальный идентификатор игры
    uuid: Mapped[str] = mapped_column(String, unique=True, default=lambda: str(uuid4()))

    # Игроки
    white: Mapped[Optional[int]] = mapped_column(nullable=True)  # ID игрока, играющего за белых
    black: Mapped[Optional[int]] = mapped_column(nullable=True)  # ID игрока, играющего за черных

    # Результат игры (0 - не завершена, 1 - белые победили, 2 - черные победили, 3 - ничья)
    result: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=False)

    # Ходы игры
    board: Mapped[List[List[str]]] = mapped_column(JSON, default=list)  # Список ходов в формате "e2-e4"

    # Дополнительные параметры игры
    game_time: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Общее время на партию (в минутах)
    increment: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Добавление времени после каждого хода (в секундах)

    # Времена таймеров для игроков
    # white_timer: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    # black_timer: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Текущий ход
    current_player_color: Mapped[str] = mapped_column(String, default="white", nullable=False)  # "white" или "black"

    # Статус игры (идет/завершена)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return (
            f"<Game(uuid={self.uuid}, white={self.white}, black={self.black}, result={self.result}, "
            f"moves={self.moves}, current_player_color={self.current_player_color})>"
        )
