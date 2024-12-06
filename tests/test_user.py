import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from repositories.user_repository import UserRepository
from config.settings import init_database
from fastapi.testclient import TestClient
from neomodel import config, db
from main import create_app
from models.user import User

class CustomTestClient(TestClient):
    def delete_with_payload(self,  **kwargs):
        return self.request(method="DELETE", **kwargs)

init_database()
app = create_app()
user_repository = UserRepository(db)
client = CustomTestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    db.cypher_query("MATCH (n) DETACH DELETE n")

def test_get_user_id_by_email():
    user = create_user()
    response = client.get(f"/api/v1/users/auth?email={user.email}")
    assert response.status_code == 200
    assert response.json().get("uid") == user.uid

def test_get_my_user():
    user = create_user()
    print(user)
    headers = {"user_id": user.uid}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_edit_my_user():
    user = create_user()
    headers = {"user_id": user.uid}
    data = {
        "username": "updateduser",
        "phone": "0987654321",
        "country": "BR",
        "description": "newdescription"
    }
    response = client.patch("/api/v1/users/me", data=data, headers=headers)
    assert response.status_code == 200
    updated_user = user_repository.find_user_by_id(user.uid)
    assert updated_user.username == "updateduser"
    assert updated_user.phone == "0987654321"
    assert updated_user.country == "BR"
    assert updated_user.description == "newdescription"

def test_get_user_by_id():
    user = create_user()
    headers = {"user_id": user.uid}
    response = client.get(f"/api/v1/users/{user.uid}", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_follow():
    # user1 follows user2, then user2 should be in user1's following list
    user1 = create_user(username="testuser1", email="Test1")
    user2 = create_user(username="testuser2", email="Test2")
    headers = {"user_id": user1.uid}
    data = {"id": user2.uid}
    # response = client.post("/api/v1/users/me/following", json=data, headers=headers)
    user1.following.connect(user2)
    user1 = user_repository.find_user_by_id(user1.uid)
    user2 = user_repository.find_user_by_id(user2.uid)
    assert user2 in user1.following
    assert user1 in user2.followers

def test_unfollow():
    # user1 unfollows user2, then user2 should not be in user1's following list
    user1 = create_user(username="testuser1", email="Test1")
    user2 = create_user(username="testuser2", email="Test2")
    headers = {"user_id": user1.uid}
    data = {"id": user2.uid}
    user1.following.connect(user2)
    response = client.delete_with_payload(url = "/api/v1/users/me/following", json=data, headers=headers)
    user1 = user_repository.find_user_by_id(user1.uid)
    user2 = user_repository.find_user_by_id(user2.uid)
    assert response.status_code == 204
    assert user2 not in user1.following
    assert user1 not in user2.followers

def test_search_user_by_username():
    user1 = create_user(username="testuser1", email="Test1")
    user2 = create_user(username="testuser2", email="Test2")
    response = client.get(url = f"api/v1/users/?username=t&offset=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_following():
    user1 = create_user(username="testuser1", email="Test1")
    user2 = create_user(username="testuser2", email="Test2")
    user1.following.connect(user2)
    headers = {"user_id": user1.uid}
    response = client.get(url = "/api/v1/users/me/following", headers=headers)
    assert response.status_code == 200
    print(response.json())
    assert response.json()["following"][0]["username"] == "testuser2"

def test_get_followers():
    user1 = create_user(username="testuser1", email="Test1")
    user2 = create_user(username="testuser2", email="Test2")
    user1.following.connect(user2)
    headers = {"user_id": user2.uid}
    response = client.get("/api/v1/users/me/followers", headers=headers)
    assert response.status_code == 200
    assert response.json()["followers"][0]["username"] == "testuser1"

def test_get_user_by_username():
    user = create_user(username = "testuser")
    user_from_db = user_repository.get_user_by_username(user.username)
    assert user_from_db.username == user.username
# utils
def register_test_user(username="testuser", email="testuser@example.com", phone="1234567890", password="stringst"):
    data = {
        "username": username,
        "email": email,
        "password": password,
        "phone": phone,
        "country": "AR"
    }
    response = client.post("/api/v1/register", json=data)
    return (response.json(), password)

def create_user(username="testuser", email="testuser@example.com", phone="1234567890", country="AR"):
    user = User(username=username, email=email, phone=phone,country=country)
    user_repository.save(user)
    return user

