import pytest
from routes import app, connection
import database as database

@pytest.fixture()
def client():
    with app.test_client() as client:
        database.clear_users_table(connection)
        yield client

class TestCreateUserRoute:
    strong_password = 'Str0ngPassword1'

    def test_create_user_success(self, client):
        response = client.post('/users', json={'username': 'testuser', 'password': self.strong_password})
        assert response.status_code == 201
        assert response.json['message'] == 'User added successfully' 

    def test_create_user_duplicate_user(self, client): 
        client.post('/users', json={'username': 'testuser', 'password': self.strong_password})
        response = client.post('/users', json={'username': 'testuser', 'password': 'AnotherPassword1'})
        assert response.status_code == 409
        assert response.json['error'] == 'User already exists' 

    def test_create_user_missing_username(self, client): 
        response = client.post('/users', json={'password': self.strong_password})
        assert response.status_code == 400
        assert response.json['error'] == 'Missing username'

    def test_create_user_missing_password(self, client): 
        response = client.post('/users', json={'username': 'testuser'})
        assert response.status_code == 400
        assert response.json['error'] == 'Missing password' 

    def test_create_user_no_json_data(self, client): 
        response = client.post('/users', json={})
        assert response.status_code == 400
        assert response.json['error'] == 'Missing username and password' 

    def test_create_user_invalid_username(self, client): 
        response = client.post('/users', json={'username': 'us', 'password': self.strong_password})
        assert response.status_code == 400
        assert response.json['error'] == 'Invalid username (must be 3-20 characters)'

    def test_create_user_invalid_password(self, client): 
        response = client.post('/users', json={'username': 'testuser', 'password': 'Weak1'})
        assert response.status_code == 400
        assert response.json['error'] == 'Invalid password (must be >=8 chars, with upper, lower, digit)'

class TestDeleteUserRoute:
    strong_password = 'Str0ngPassword1'
    username = 'deleteuser'

    def test_delete_user_success(self, client):
        client.post('/users', json={'username': self.username, 'password': self.strong_password})
        response = client.delete('/users', json={'username': self.username, 'password': self.strong_password})
        assert response.status_code == 200
        assert response.json['message'] == 'User deleted successfully'

    def test_delete_user_invalid_password(self, client):
        client.post('/users', json={'username': self.username, 'password': self.strong_password})
        response = client.delete('/users', json={'username': self.username, 'password': 'WrongPassword1'})
        assert response.status_code == 401
        assert response.json['error'] == 'Invalid username or password'

    def test_delete_user_non_existent_user(self, client):
        response = client.delete('/users', json={'username': 'nosuchuser', 'password': self.strong_password})
        assert response.status_code == 401
        assert response.json['error'] == 'Invalid username or password'

    def test_delete_user_missing_username(self, client):
        response = client.delete('/users', json={'password': self.strong_password})
        assert response.status_code == 400
        assert response.json['error'] == 'Missing username'

    def test_delete_user_missing_password(self, client):
        response = client.delete('/users', json={'username': self.username})
        assert response.status_code == 400
        assert response.json['error'] == 'Missing password'

class TestLoginRoute:
    strong_password = 'Str0ngPassword1'
    username = 'loginuser'

    def test_login_success(self, client):
        client.post('/users', json={'username': self.username, 'password': self.strong_password})
        response = client.get('/login', json={'username': self.username, 'password': self.strong_password})
        assert response.status_code == 200
        assert response.json['message'] == 'Login successful'

    def test_login_invalid_password(self, client):
        client.post('/users', json={'username': self.username, 'password': self.strong_password})
        response = client.get('/login', json={'username': self.username, 'password': 'WrongPassword1'})
        assert response.status_code == 401
        assert response.json['error'] == 'Invalid username or password'

    def test_login_non_existent_user(self, client):
        response = client.get('/login', json={'username': 'nosuchuser', 'password': self.strong_password})
        assert response.status_code == 401
        assert response.json['error'] == 'Invalid username or password'

    def test_login_missing_username(self, client):
        response = client.get('/login', json={'password': self.strong_password})
        assert response.status_code == 400
        assert response.json['error'] == 'Missing username'

    def test_login_missing_password(self, client):
        response = client.get('/login', json={'username': self.username})
        assert response.status_code == 400
        assert response.json['error'] == 'Missing password'

    def test_login_no_json_data(self, client):
        response = client.get('/login', json={})
        assert response.status_code == 400
        assert response.json['error'] == 'Missing username and password'
