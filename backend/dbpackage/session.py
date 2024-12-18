from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pkgs.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_NAME
print("Database URL is ",SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
