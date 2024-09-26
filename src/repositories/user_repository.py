from models.user import User
from neomodel import db

class UserRepository:
    def __init__(self, database = db):
        self.database = database

    def create_user(self, user)-> User:
        return user.save()
    
    def find_user_by_email(self, email):
        try:
            user = User.nodes.get( email = email)
            return user
        except User.DoesNotExist:
            return None
        
    def find_user_by_id (self, id ):
        try:
            user = User.nodes.get( uid = id)
            return user
        except User.DoesNotExist:
            return None

    def get_all_users (self):
        return User.nodes.all()
    
    def update_user(self, user):
        return user.save()

user_repository = UserRepository()