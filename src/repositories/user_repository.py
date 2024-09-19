from models.user import User
from neomodel import db

class UserRepository:
    def __init__(self, database = db):
        self.database = database

    def create_user(self, user)-> User:
        return user.save()
    
    def find_user_by_mail(self, mail):
        try:
            user = User.nodes.get( mail = mail)
            return user
        except User.DoesNotExist:
            return None
        
user_repository = UserRepository()