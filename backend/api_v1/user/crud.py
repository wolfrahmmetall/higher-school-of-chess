"""
Create
Read
Update
Delete
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from .schemas import CreateUser
from .User import User

async def create_user(session: AsyncSession, user_in: CreateUser):
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user

async def get_users(session: AsyncSession) -> list[User]:
    query = select(User).group_by(User.login)
    result: Result = await session.execute(query)
    users = result.scalars().all()
    return list(users)

async def get_user(session: AsyncSession, uid: str):
    return await session.get(User, uid)