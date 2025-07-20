import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_connection():
    response = client.get("/connect?host=127.0.0.1&username=root")

    assert response.status_code == 200
    assert response.json() == { "error": "Unable to connect 127.0.0.1 on port 127.0.0.1"}

def test_add_server():
    response = client.get("/connect?host=my_server&username=base_user")
    assert response.status_code == 200
    assert response.json() == { "response": "base_user\n" }

    response_2 = client.get("/all_servers")

    assert response_2.status_code == 200
