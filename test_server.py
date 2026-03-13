from fastapi.testclient import TestClient 
from server import app

client = TestClient(app)

def test_ping_success():
	response = client.get("/8.8.8.8")
	assert response.status_code == 200
	data = response.json()
	assert "1 received" in data["result"] 

def test_ping_failure():
	response = client.get("/192.0.2.1")
	assert response.status_code == 200
	data = response.json()
	assert "0 received" in data["result"]
