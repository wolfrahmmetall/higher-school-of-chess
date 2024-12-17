from typing import Optional
from uuid import uuid4
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.sqlite import JSON
from dbpackage.Base import Base

class Games(Base):
    # Публичный идентификатор (uuid), который не является первичным ключом
    # id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String, unique=True, default=lambda: str(uuid4()))

    # Данные игры
    white: Mapped[Optional[int]] = mapped_column(nullable=True)  # ID игрока (int)
    black: Mapped[Optional[int]] = mapped_column(nullable=True)  # ID игрока (int)
    result: Mapped[Optional[int]] = mapped_column(nullable=True)  # Результат игры
    moves: Mapped[list] = mapped_column(JSON)  # Ходы игры (храним как JSON)

# 2024-12-17 18:48:09,871 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2024-12-17 18:48:09,873 INFO sqlalchemy.engine.Engine SELECT user.login, user.password, user.email, user.elo_score, user.id 
# FROM user 
# WHERE user.login = ?
# 2024-12-17 18:48:09,874 INFO sqlalchemy.engine.Engine [generated in 0.00011s] ('string',)
# 2024-12-17 18:48:09,875 INFO sqlalchemy.engine.Engine INSERT INTO user (login, password, email, elo_score) VALUES (?, ?, ?, ?)
# 2024-12-17 18:48:09,875 INFO sqlalchemy.engine.Engine [generated in 0.00008s] ('string', <memory at 0x1045750c0>, 'user@example.com', 1000.0)
# 2024-12-17 18:48:09,875 INFO sqlalchemy.engine.Engine COMMIT
# INFO:     127.0.0.1:50465 - "POST /users/register HTTP/1.1" 200 OK