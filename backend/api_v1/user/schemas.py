from datetime import date
from typing import Annotated
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    login : str #equivalent to UID. To be used that way 
    # TODO: update the key to be an uuid, login is to be used as a mean to get it
    email : str
    elo_score : float

    

class CreateUser(UserBase):
    ...

class UpdateUser(CreateUser):
    ...


class UserUpdatePartial(CreateUser):
    name: str | None = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)