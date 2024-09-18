from models.user import User
from neomodel import db

class UserRepository:
    def __init__(self, database=db):
        self.database = database

    def create_user(self, user)-> User:
        return user.save()

user_repository = UserRepository()