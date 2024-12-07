import pytest
from api_v1.auth.utils import hash_password, validate_password

@pytest.mark.parametrize("password", [
    "password123",
    "my_secure_password",
    "12345678",
    "another_password!"
])
def test_hash_password(password):
    hashed = hash_password(password)
    assert hashed is not None
    assert isinstance(hashed, bytes)

def test_validate_password():
    password = "secure_password"
    hashed = hash_password(password)

    assert validate_password(password, hashed) is True
    assert validate_password("wrong_password", hashed) is False