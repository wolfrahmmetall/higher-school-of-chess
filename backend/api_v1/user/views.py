from typing import Annotated
from annotated_types import MaxLen, MinLen
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .schemas import User, CreateUser
from dbpackage.DBHelper import db_helper


router = APIRouter(tags=['Users'])


@router.get('/', response_model=list[User])
async def get_users(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_users(session=session)


@router.post('/', response_model=User)
async def create_user(user_in: CreateUser, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.create_user(user_in=user_in, session=session)

@router.get('/{user_id}', response_model=User)
async def get_user(user_id, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user = await crud.get_user(session=session, uid=user_id)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'{user_id} not found'
    )