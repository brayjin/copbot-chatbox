import pytest
from fastapi.testclient import TestClient
from CopBotChatbox.main import app

client = TestClient(app)

def test_get_procedures():
    response = client.get("/procedures")
    assert response.status_code == 200
    data = response.json()
    assert "procedures" in data

def test_query_handler():
    response = client.post("/query", json={"query": "Test query"})
    assert response.status_code == 200
    data = response.json()
    assert "rasa_response" in data
