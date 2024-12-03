import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
from dbpackage.DBHelper import db_helper_user
from .schemas import CreateUser
from .crud import create_user, get_user_by_login, delete_user_by_id

app = FastAPI()

@pytest.mark.asyncio
async def test_create_user():
    async for session in db_helper_user.session_dependency():
        user_data = CreateUser(login="testuser", password="password123", email="test@example.com")

        existing_user = await get_user_by_login(session, user_data.login)
        if existing_user:
            await delete_user_by_id(session, existing_user.id)

        user = await create_user(session, user_data)
        assert user.login == "testuser"
        assert user.email == "test@example.com"

@pytest.mark.asyncio
async def test_get_user_by_login():
    async for session in db_helper_user.session_dependency():
        user_data = CreateUser(login="testuser2", password="password123", email="test2@example.com")
        
        existing_user = await get_user_by_login(session, user_data.login)
        if existing_user:
            await delete_user_by_id(session, existing_user.id)

        await create_user(session, user_data)
        user = await get_user_by_login(session, "testuser2")
        assert user is not None
        assert user.login == "testuser2"

@pytest.mark.asyncio
async def test_delete_user_by_id():
    async for session in db_helper_user.session_dependency():
        user_data = CreateUser(login="testuser3", password="password123", email="test3@example.com")

        existing_user = await get_user_by_login(session, user_data.login)
        if existing_user:
            await delete_user_by_id(session, existing_user.id)

        user = await create_user(session, user_data)
        await delete_user_by_id(session, user.id)
        deleted_user = await get_user_by_login(session, "testuser3")
        assert deleted_user is None