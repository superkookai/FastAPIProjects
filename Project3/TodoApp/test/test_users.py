from .utils import *
from TodoApp.routers.users import get_db,get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user/current")
    assert response.status_code == 200
    assert response.json()["username"] == "codingwithrobytest"
    assert response.json()["email"] == "codingwithrobytest@email.com"
    assert response.json()["first_name"] == "Eric"
    assert response.json()["last_name"] == "Roby"
    assert bcrypt_context.verify("testpassword",response.json()["hashed_password"]) is True


def test_change_password_success(test_user):
    response = client.put("/user/change_password",json={"password":"testpassword","new_password":"newpassword"})
    assert response.status_code == 204


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/change_password", json={"password": "test", "new_password": "newpassword"})
    assert response.status_code == 404
    assert response.json() == {"detail":"Password not match"}


def test_change_phone_number_success(test_user):
    response = client.put("/user/change/9876543210")
    assert response.status_code == 204







