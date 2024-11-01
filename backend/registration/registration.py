from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from sqlalchemy import MetaData
from pkgs.config import settings
from dbpackage.DBHelper import db_helper
from dbpackage import Base

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(MetaData().create_all)
    yield



app = FastAPI()

@app.get('/')
def hello_api():
    return {'msg':'hello_api'}

@app.get('/items')
def show_leaderboard():
    return ('Aalik', 'IvanZ')

if __name__ == '__main__':
    uvicorn.run("registration:app", reload=True)
 