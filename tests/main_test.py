import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_connection():
    response = client.get("/connect?host=1.1.1.1&username=root")

    assert response.status_code == 200
    assert response.json() == { "error": "Error while try to connect server! Please check hostname!" }

