
from fastapi.testclient import TestClient
from TodoApp.main import app
from fastapi import status
# import sys
# print("Python sys.path:", sys.path)

client = TestClient(app)

def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status":"healthy"}