from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from pkgs.config import settings
from dbpackage.DBHelper import db_helper
from dbpackage.Base import Base
from api_v1 import router as router_v1
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

@app.get('/')
def hello_api():
    return {'msg':'hello_api'}

@app.get('/items')
def show_leaderboard():
    return ('Aalik', 'IvanZ')

if __name__ == '__main__':
    # path = Path('backend/databases').resolve()
    # print(path)
    # print(path.is_dir())
    uvicorn.run("registration:app", reload=True)
    # print(Path(__file__).parent)