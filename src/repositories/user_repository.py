from models.user import User
from neomodel import db

class UserRepository:
    def __init__(self, database = db):
        self.database = database

    @db.transaction
    def save(self, user)-> User:
        return user.save()
    
    @db.transaction
    def find_user_by_email(self, email):
        try:
            user = User.nodes.get( email = email)
            return user
        except User.DoesNotExist:
            return None
        
    @db.transaction    
    def find_user_by_id (self, id )-> User:
        try:
            user = User.nodes.get( uid = id)
            return user
        except User.DoesNotExist:
            return None
    
    @db.transaction
    def get_users_by_username(self, username: str, offset: int, limit: int):
        if not username:
            return []
        username = username.lower()
        query = "MATCH (u:User) WHERE toLower(u.username) STARTS WITH $username AND u.is_banned = false"
        query += " RETURN u SKIP $offset LIMIT $limit"
        parameters = {
            "username": username,
            "offset": offset,
            "limit": limit
        }
        results, _ = db.cypher_query(query, parameters)
        return [User.inflate(record[0]) for record in results]
    
    @db.transaction
    def get_all_users(self, offset: int, limit: int):
        query = "MATCH (u:User) RETURN u SKIP $offset LIMIT $limit"
        parameters = {
            "offset": offset,
            "limit": limit
        }
        results, _ = db.cypher_query(query, parameters)
        return [User.inflate(record[0]) for record in results]
     
user_repository = UserRepository()