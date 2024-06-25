from fastapi.testclient import TestClient
from fastapi import status
from ..main import app

client = TestClient(app)

def test_health_checkup():
    res = client.get('/healthy')
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {'status':'Healthy'}
    