from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = 'sqlite+aiosqlite:///../databases'
    
settings = Settings()

if __name__ == '__main__':
    print(env_path.exists())
    print(settings.DATABASE_URL)