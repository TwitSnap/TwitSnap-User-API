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


init_database()
app = create_app()
user_repository = UserRepository(db)
client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    db.cypher_query("MATCH (n:User) DETACH DELETE n")


def test_ban_or_unban_user():

    user = create_user()
    response = client.post(url = f"/api/v1/admin/users/{user.uid}/ban")
    user = user_repository.find_user_by_id(user.uid)
    assert response.status_code == 204
    assert user.is_banned == True


    response = client.post(url = f"/api/v1/admin/users/{user.uid}/ban")
    assert response.status_code == 204
    user = user_repository.find_user_by_id(user.uid)
    assert user.is_banned == False

def test_get_all_users():
    user = create_user()
    response = client.get(url = f"/api/v1/admin/users",)
    assert response.status_code == 200
    assert response.json()["total_users"] == 1

def create_user(username="testuser", email="testuser@example.com", phone="1234567890", country="AR"):
    user = User(username=username, email=email, phone=phone,country=country)
    user_repository.save(user)
    return user