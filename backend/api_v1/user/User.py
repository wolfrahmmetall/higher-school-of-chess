from datetime import date
from typing import Annotated
from annotated_types import MaxLen, MinLen
from pydantic import EmailStr
from sqlalchemy.orm import Mapped
from dbpackage.Base import Base


class User(Base):
    """
    Базовый класс пользователя -- хранит его логин и почту. 
    Логин используется как User ID во всех БД
    """
    login : Mapped[str] #equivalent to UID. To be used that way 
    # TODO: update the key to be an uuid, login is to be used as a mean to get it
    email : Mapped[str]
    elo_score : Mapped[float]

