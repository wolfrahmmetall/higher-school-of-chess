from datetime import date
from typing import Annotated
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr
from sqlalchemy import Date

class User(BaseModel):
    """
    Базовый класс пользователя -- хранит его логин и почту. 
    Логин используется как User ID во всех БД
    """
    login : Annotated[str, MinLen(7), MaxLen(30)] #equivalent to UID. To be used that way 
    email : EmailStr
    registration_date: date
    elo_score : float

