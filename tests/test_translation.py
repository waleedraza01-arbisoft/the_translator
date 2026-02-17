from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "active", "service": "the_translator"}

def test_translation_flow():
    # We test with a simple phrase
    payload = {"text": "Hello world"}
    response = client.post("/translate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "translation" in data
    # The model should translate "Hello world" to something containing "Bonjour"
    assert "Bonjour" in data["translation"]