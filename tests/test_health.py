from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["agents"] == ["Query Analyzer", "Research Agent", "Answer Reviewer"]

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Research Analyst Assistant" in response.text
