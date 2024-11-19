"""
Create
Read
Update
Delete
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from fastapi import HTTPException, status

from dbpackage.DBHelper import db_helper_user
from .schemas import CreateUser
from .User import User #, Auth
from api_v1.auth.utils import hash_password

async def get_users(session: AsyncSession) -> list[User]:
    query = select(User).group_by(User.login)
    result: Result = await session.execute(query)
    users = result.scalars().all()
    return list(users)

async def get_user_by_id(session: AsyncSession, uid: int):
    return await session.get(User, uid)

async def get_user_by_login(session: AsyncSession, login:str):
    query = select(User).where(User.login == login)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    return user


async def delete_user(session: AsyncSession, user: User):
    if user is not None:
        print(user.id)
        await session.delete(user)
        await session.commit()

async def delete_user_by_id(session:AsyncSession, uid: int) -> None:
    user = await get_user_by_id(session=session, uid=uid)
    print(user.id)
    await delete_user(session=session, user=user)


async def create_user(session_user: AsyncSession, user_in: CreateUser):
    user_in.elo_score = 1000
    user = User(**user_in.model_dump())
    user.password = hash_password(user.password)
    query = select(User).where(User.login == user.login)
    result = await session_user.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="User already exists")

    session_user.add(instance=user)
    # session_auth.add(instance=auth)

    await session_user.commit()
    # await session_auth.commit()

    return user


if __name__ == '__main__':
    import asyncio
    async def af():
        u: dict = {'login': 'Ultimate',
                    "email": 'user@example.com',
                    'elo_score': 42.923}
        
        user = CreateUser(**u)
        res = await create_user(db_helper_user.get_scoped_session(), user)
        print(res.login, res.email)

    asyncio.run(af())
