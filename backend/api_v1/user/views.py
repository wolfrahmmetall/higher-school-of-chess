from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .schemas import User, CreateUser, LoginUser
from dbpackage.DBHelper import db_helper_user
from jose import jwt
from datetime import datetime, timedelta
from api_v1.auth.utils import validate_password
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=['Users'])



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

@router.post('/login', response_model=dict)
async def login(user_in: LoginUser, session: AsyncSession = Depends(db_helper_user.scoped_session_dependency)):
    print("Полученные данные для логина:", user_in)
    # Ищем пользователя по логину
    user = await crud.get_user_by_login(session=session, login=user_in.login)
    print("Пользователь из базы данных:", user)
    
    if user is None:
        print("Ошибка: пользователь не найден")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )
    
    # Проверяем пароль
    print("Введённый пароль:", user_in.password)
    print("Хранимый хэш пароля:", user.password)
    
    if not validate_password(user_in.password, user.password):
        print("Ошибка: пароли не совпадают")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )
    
    # Создаем токен
    token_data = {
        "sub": str(user.id),  # Используем ID пользователя в качестве идентификатора
        "login": user.login,  # Дополнительная информация
    }
    token = create_access_token(data=token_data)
    print("Токен успешно создан:", token)

    return {"access_token": token}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(db_helper_user.scoped_session_dependency)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Не удалось подтвердить учетные данные")
        
        # Проверяем пользователя в базе данных
        user = await crud.get_user_by_id(session, user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        
        return user
    except ExpiredSignatureError:
        print(f"Token expired: {token}")
        raise HTTPException(status_code=401, detail="Токен истек")
    except JWTError as e:
        print(f"JWTError: {str(e)}")
        print(f"Token received: {token}")
        raise HTTPException(status_code=401, detail="Не удалось подтвердить учетные данные")

