from fastapi.testclient import TestClient 
from server import app

client = TestClient(app)

def test_ping_success():
	"""Verify the ping endpoint returns a successful ping result for a reachable host."""
	response = client.get("/8.8.8.8")
	assert response.status_code == 200
	data = response.json()
	assert "1 received" in data["result"] 

def test_ping_failure():
	"""Verify the ping endpoint returns a failed ping result for an unreachable host."""
	response = client.get("/192.0.2.1")
	assert response.status_code == 200
	data = response.json()
	assert "0 received" in data["result"]
