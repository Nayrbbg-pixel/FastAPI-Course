from ..main import app
from ..routers.todos import get_db, authorize
from fastapi.testclient import TestClient
from fastapi import status
from .utils import *

app.dependency_overrides[get_db] = overrides_get_db
app.dependency_overrides[authorize] = overrides_authorize

client = TestClient(app)




def test_todos_component(test_todo_cre_del):
    rs = client.get('/todo/1')
    assert rs.status_code == status.HTTP_200_OK
    assert rs.json() == {
                        'title':'Test todo','description':'This is a test todo',
                        'priority':4,'complete':False,'owner_id':1,'id':1
                        }
    

def test_todo_not_found():
    rs = client.get('/todo/23')
    assert rs.status_code == status.HTTP_404_NOT_FOUND
    assert rs.json() == {'detail':'Todo not found'}

def test_create_todo(test_todo_cre_del):
    data = {
            'title':'New Test todo',
            'description':'This is a new test todo',
            'priority':5,
            'complete':False
            }
    
    rs = client.post('/create-todo',json=data)
    assert rs.status_code == 201
    assert rs.json() == {
            'status':'Success!'
            }
    

def test_update_todo(test_todo_cre_del):
    data = {
        'title':'this is the updated todo'
    }

    rs = client.put('/update-todo/1',json=data)
    assert rs.status_code == 200
    assert 'title' in rs.json()
    assert rs.json()['title'] == 'this is the updated todo'

def test_update_todo_not_found(test_todo_cre_del):
    data = {
        'title':'this is the updated todo'
    }

    rs = client.put('/update-todo/999',json=data)
    assert rs.status_code == 404
    assert 'detail' in rs.json()
    assert rs.json()['detail'] == 'Todo not found!'

def test_delete_todos(test_todo_cre_del):
    rs = client.delete('/delete-todo/1')
    assert rs.status_code == 200
    db = TestingSessionLocal()
    model = db.query(Todos).get(1)
    assert model is None

def test_delete_todos_not_found(test_todo_cre_del):
    rs = client.delete('/delete-todo/999')
    assert rs.status_code == 404
    assert rs.json() == {'detail':'Todo item not found'}