from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'api_v1' / 'certificates' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'api_v1' / 'certificates' / 'jwt-public.pem'
    algorithm: str= 'RS256'
    access_token_lifetime: int = 15
    

class SettingsAuth(BaseSettings):
    api_v1_prefix: str = '/api/v1'
    DATABASE_ECHO: bool = True
    auth_jwt: AuthJWT = AuthJWT()
    DATABASE_NAME: str = f'sqlite+aiosqlite:///{BASE_DIR}/databases/auth.db'
settings_auth = SettingsAuth()


class SettingsUsers(BaseSettings):
    DATABASE_ECHO: bool = True
    DATABASE_NAME: str = f'sqlite+aiosqlite:///{BASE_DIR}/databases/user.db'
settings_user = SettingsUsers('users')

if __name__ == '__main__':
    print(settings_auth.DATABASE_NAME)
    # print(os.getenv("POSTGRES_USER"))
