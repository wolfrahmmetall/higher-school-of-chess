from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pkgs.config import settings_auth, settings_games

Base = declarative_base()

SQLALCHEMY_AUTH_DB_URL = settings_auth.DATABASE_NAME
print("Database URL is ",SQLALCHEMY_AUTH_DB_URL)
engine = create_engine(SQLALCHEMY_AUTH_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SQLALCHEMY_GAME_DB_URL = settings_games.DATABASE_NAME
game_engine = create_engine(SQLALCHEMY_GAME_DB_URL)
SessionLocal_game = sessionmaker(autocommit=False, autoflush=False, bind=game_engine)
