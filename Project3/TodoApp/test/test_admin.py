from .utils import *
from TodoApp.routers.admin import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == 200
    assert response.json() == [{
        "id":1,
        "title":"Learn to code",
        "description":"Need to learn everyday",
        "priority":5,
        "complete":False,
        "owner_id": 1
    }]


def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id==1).first()
    assert model is None


def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail":"Todo not found"}
