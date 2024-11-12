"""
Create
Read
Update
Delete
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from dbpackage.DBHelper import db_helper
from .schemas import CreateUser
from .User import User

async def create_user(session: AsyncSession, user_in: CreateUser):
    user = User(**user_in.model_dump())
    # print(type(user))
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

if __name__ == '__main__':
    import asyncio
    async def af():
        u: dict = {'login': 'Ultimate',
                    "email": 'user@example.com',
                    'elo_score': 42.923}
        
        user = CreateUser(**u)
        res = await create_user(db_helper.get_scoped_session(), user)
        print(res.login, res.email)

    asyncio.run(af())