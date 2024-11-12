from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    api_v1_prefix: str = '/api/v1'
    DATABASE_NAME: str = f'sqlite+aiosqlite:///{BASE_DIR}/databases/auth.db'
    DATABASE_ECHO: bool = True

    
settings = Settings()

if __name__ == '__main__':
    print(settings.DATABASE_NAME)
    # print(os.getenv("POSTGRES_USER"))
