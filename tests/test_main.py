import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to AI Agent Assistant!"}

def test_handle_query_valid():
    payload = {
        "query": "What is the capital of France?",
        "context": {"sector": "general"}
    }
    response = client.post("/query", json=payload)
    assert response.status_code == 200
    assert "response" in response.json()

def test_handle_query_invalid():
    payload = {"invalid": "data"}
    response = client.post("/query", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
