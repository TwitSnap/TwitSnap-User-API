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
    @db.transaction
    def get_users_by_username(self, username: str, offset: int, limit: int):
        query = "MATCH (u:User)"
        if username:
            query += " WHERE u.username CONTAINS $username"
        query += " RETURN u SKIP $offset LIMIT $limit"
        parameters = {
            "username": username,
            "offset": offset,
            "limit": limit
        }
        results, _ = db.cypher_query(query, parameters)
        return [User.inflate(record[0]) for record in results]
     
user_repository = UserRepository()