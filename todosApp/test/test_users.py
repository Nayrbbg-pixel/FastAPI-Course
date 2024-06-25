from .utils import *
from ..routers.Users import get_db, authorize
from ..main import app
from fastapi.testclient import TestClient

app.dependency_overrides[get_db] = overrides_get_db
app.dependency_overrides[authorize] = overrides_authorize

client = TestClient(app)

def test_profile(test_user):
    rs = client.get('/user/profile')
    assert rs.status_code == 200
    
def test_change_password(test_user):
    data = {'current_password':'testUser',
            'new_password':'testUser1234',
            'confirmed_password':'testUser1234'}
    rs = client.put('/user/change-password',json=data)
    assert rs.status_code == 200
    assert rs.json() == {'status':'Success'}

def test_invalid_change_password(test_user):
    data = {'current_password':'testUser12',
            'new_password':'testUser1234',
            'confirmed_password':'testUser1234'
            }
    
    rs = client.put('/user/change-password',json=data)
    assert rs.status_code == 401
    assert rs.json() == {'detail':'The current password you entered was wrong.'}

def test_phone_number_change(test_user):
    data = {
        "phone_number":'0987654321'
    }

    rs = client.put('/user/update-phone-number',json=data)
    assert rs.status_code == 200
    assert rs.json() == {'status':'Success'}