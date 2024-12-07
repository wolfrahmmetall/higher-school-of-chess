import bcrypt
import jwt

from pkgs.config import settings_auth

def encode_jwt(
        payload: dict,
        key = settings_auth.auth_jwt.private_key_path.read_text(),
        algorithm=settings_auth.auth_jwt.algorithm,
        expire_min: int = settings_auth.auth_jwt.access_token_lifetime
):
    to_encode = payload.copy()
    to_encode.update(exp = expire_min)
    encoded = jwt.encode(
        payload,
        key,
        algorithm
    )
    return encoded

def decode_jwt(
        token: str | bytes,
        public_key = settings_auth.auth_jwt.public_key_path.read_text(), 
        algorithm=settings_auth.auth_jwt.algorithm
):
    decoded = jwt.decode(
        token, public_key, algorithms=[algorithm]
    )
    return decoded

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def validate_password(password: str , hash: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hash)

# TODO: code CRUDs for logging users in + its DB.
# TODO: After that create a blank html page with proper forms and redirection buttons. The design is on Alik