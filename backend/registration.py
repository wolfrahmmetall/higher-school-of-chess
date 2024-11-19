from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from dbpackage.DBHelper import db_helper_user
from dbpackage.Base import Base
from api_v1 import router as router_v1
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper_user.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1)

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://localhost:8080",
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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