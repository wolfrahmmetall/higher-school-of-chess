from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    login : str #equivalent to UID. To be used that way 
    password : str
    email : EmailStr
    elo_score : float | None

class CreateUser(UserBase):
    elo_score: float = 1000

class UpdateUser(CreateUser):
    ...

class LoginUser(BaseModel):
    login : str
    password : str

class UserUpdatePartial(CreateUser):
    name: str | None = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True