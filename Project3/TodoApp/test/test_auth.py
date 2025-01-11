from .utils import *
from TodoApp.routers.auth import get_db,authenticate_user,create_access_token,SECRET_KEY,ALGORITHM,get_current_user
from jose import jwt
from datetime import timedelta,datetime,timezone
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username,"testpassword",db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_exist_user = authenticate_user("WrongUsername","testpassword",db)
    assert non_exist_user is False

    wrong_password_user = authenticate_user(test_user.username,"WrongPassword",db)
    assert wrong_password_user is False


def test_create_access_token(test_user):
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username,user_id,role,expires_delta)
    decoded_token = jwt.decode(token,SECRET_KEY,[ALGORITHM],options={"verify_signature":False})

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role
    assert decoded_token["exp"] == int((expires_delta+datetime.now(timezone.utc)).timestamp())


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub":"testuser","id":1,"role":"admin"}
    token = jwt.encode(encode,SECRET_KEY,ALGORITHM)
    user = await get_current_user(token)
    assert user == {"username":"testuser","id":1,"user_role":"admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role":"user"}
    token = jwt.encode(encode,SECRET_KEY,ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not valid user!"
