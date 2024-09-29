from models.user import User
from neomodel import db

class UserRepository:
    def __init__(self, database = db):
        self.database = database

    @db.transaction
    def create_user(self, user)-> User:
        return user.save()
    
    @db.transaction
    def find_user_by_email(self, email):
        try:
            user = User.nodes.get( email = email)
            return user
        except User.DoesNotExist:
            return None
        
    @db.transaction    
    def find_user_by_id (self, id ):
        try:
            user = User.nodes.get( uid = id)
            return user
        except User.DoesNotExist:
            return None

    @db.transaction
    def get_all_users (self):
        return User.nodes.all()
    
    @db.transaction
    def update_user(self, user):
        return user.save()
    
    @db.transaction
    def delete_all_users(self):
        users = User.nodes.all()
        for user in users:
            user.delete()

user_repository = UserRepository()