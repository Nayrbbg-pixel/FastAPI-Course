from .utils import *
from ..routers.admin import get_db,authorize
from ..main import app
from fastapi.testclient import TestClient

app.dependency_overrides[get_db] = overrides_get_db
app.dependency_overrides[authorize] = overrides_authorize

client = TestClient(app)

def test_get_all_todos(test_todo_cre_del):
    rs = client.get('/admin/get-todo')
    assert rs.status_code == 200
    assert rs.json() == [{
        'title':'Test todo','description':'This is a test todo',
        'priority':4,'complete':False,'owner_id':1,'id':1
        }]

def test_delete_todo(test_todo_cre_del):
    rs = client.delete('/admin/delete-todo/1')
    assert rs.status_code == 200
    assert rs.json() == {"Status":"Success"}
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo(test_todo_cre_del):
    rs = client.delete('/admin/delete-todo/999')
    assert rs.status_code == 404
    assert rs.json() == {'detail':'Todo not found'}
