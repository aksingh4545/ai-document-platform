import os

from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("CORS_ORIGINS", "*")

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Backend running"}


def test_dashboard_empty():
    response = client.get("/dashboard")
    assert response.status_code == 200
    body = response.json()
    assert body["total_documents"] == 0
    assert body["total_chunks"] == 0
    assert body["total_queries"] == 0
