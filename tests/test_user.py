import sys
import os

from config.settings import init_database

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import pytest
from fastapi.testclient import TestClient
from neomodel import config, db
from main import create_app
from models.user import User

init_database()
app = create_app()
client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    db.cypher_query("MATCH (n) DETACH DELETE n")

def test_get_user_id_by_email():
    user = User(username="testuser", email="testuser@example.com", phone="1234567890").save()
    response = client.get(f"/api/v1/users/id?email={user.email}")
    assert response.status_code == 200
    assert response.json() == user.uid

def test_get_my_user():
    user, password = register_test_user()
        
    login_data = {
        "email": user["email"],
        "password": password
    }
    response = client.post(AUTH_API_URI + AUTH_API_LOGIN_PATH, json=login_data)
    assert response.status_code == 200
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_edit_my_user():
    user, password = register_test_user()

    token = "Bearer your_token_here"
    headers = {"Authorization": f"Bearer {token}"}
    
    new_user_data = {
        "username": "updateduser",
        "phone": "0987654321",
        "country": "newcountry",
        "description": "newdescription"
    }
    
    response = client.patch("/api/v1/users/me", json=new_user_data, headers=headers)
    assert response.status_code == 200
    updated_user = User.nodes.get(uid=user['uid'])
    assert updated_user.username == "updateduser"
    assert updated_user.phone == "0987654321"
    assert updated_user.country == "newcountry"
    assert updated_user.description == "newdescription"

def test_get_user_by_id():
    user, _ = register_test_user("testuser", "testuser@example.com", "1234567890")
    
    response = client.get(f"/api/v1/users/{user['uid']}")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_get_all_users():
    user1, _ = register_test_user("testuser1", "testuser1@example.com", "1234567890")
    user2, _ = register_test_user("testuser2", "testuser2@example.com", "0987654321")
    
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 2
    assert users[0]["username"] == "testuser1"
    assert users[1]["username"] == "testuser2"

def test_delete_all_users():
    user1, _ = register_test_user("testuser1", "testuser1@example.com", "1234567890")
    user2, _ = register_test_user("testuser2", "testuser2@example.com", "0987654321")
    
    response = client.delete("/api/v1/users/")
    assert response.status_code == 204
    
    users = User.nodes.all()
    assert len(users) == 0

# utils
def register_test_user(username="testuser", email="testuser@example.com", phone="1234567890", password="stringst"):
    data = {
        "username": username,
        "email": email,
        "password": password,
        "phone": phone,
        "country": "string"
    }
    response = client.post("/api/v1/register", json=data)
    return (response.json(), password)
