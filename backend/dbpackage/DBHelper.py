from asyncio import current_task
from typing import AsyncGenerator, Any
from sqlalchemy.ext.asyncio import (create_async_engine, 
                                    async_sessionmaker, 
                                    async_scoped_session)
from pkgs.config import settings_games, settings_user
class DatabaseHelper:
    def __init__(self, url:str, echo:bool = False):
        self.engine = create_async_engine(
            url = url, 
            echo = echo
        )
        self.session_factory = async_sessionmaker(bind=self.engine, 
                                            autoflush=False, 
                                            autocommit=False, 
                                            expire_on_commit=False)
        
    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session
    
    async def session_dependency(self) -> AsyncGenerator[Any, Any]:
        session = self.get_scoped_session()
        yield session
        await session.close()

    async def scoped_session_dependency(self) -> AsyncGenerator[async_scoped_session, Any]:
        session = self.get_scoped_session()
        yield session
        await session.close()

db_helper_user = DatabaseHelper(url=settings_user.DATABASE_NAME, echo=settings_user.DATABASE_ECHO)

db_helper_game = DatabaseHelper(url=settings_games.DATABASE_NAME, echo=settings_games.DATABASE_ECHO)
