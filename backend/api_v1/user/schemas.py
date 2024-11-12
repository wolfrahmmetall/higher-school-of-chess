from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    login: str
    

class CreateUser(UserBase):
    ...

class UpdateUser(UserBase):
    ...


class UserUpdatePartial(CreateUser):
    name: str | None = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    login : str