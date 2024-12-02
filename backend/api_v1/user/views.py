from typing import Annotated
from annotated_types import MaxLen, MinLen
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import crud
from .schemas import User, CreateUser, LoginUser
from dbpackage.DBHelper import db_helper_user
from jose import jwt
from datetime import datetime, timedelta
from api_v1.auth.utils import hash_password, validate_password


router = APIRouter(tags=['Users'])


@router.get('/', response_model=list[User])
async def get_users(session: AsyncSession = Depends(db_helper_user.scoped_session_dependency)):
    return await crud.get_users(session=session)


@router.post('/register', response_model=User)
async def create_user(user_in: CreateUser,
                      #session_auth: AsyncSession = Depends(db_helper_auth.scoped_session_dependency),
                      session_user: AsyncSession = Depends(db_helper_user.scoped_session_dependency)):
    return await crud.create_user(user_in=user_in, session_user=session_user)

@router.get('/{user_id}', response_model=User)
async def get_user(user_id, session: AsyncSession = Depends(db_helper_user.scoped_session_dependency)):
    user = await crud.get_user_by_id(session=session, uid=user_id)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'{user_id} not found'
    )

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id, session: AsyncSession = Depends(db_helper_user.scoped_session_dependency)):
    await crud.delete_user_by_id(session=session, uid=user_id)

# TODO: загрузить все в .env
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Генерация токена
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Авторизация
@router.post('/login', response_model=dict)
async def login(user_in: LoginUser, session: AsyncSession = Depends(db_helper_user.scoped_session_dependency)):
    user = await crud.get_user_by_login(session=session, login=user_in.login)
    if user is None or not validate_password(user_in.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login or password")
    
    token = create_access_token({"sub": user.login})
    return {"access_token": token}