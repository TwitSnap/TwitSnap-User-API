from models.user import User
from neomodel import db

from config.settings import logger


class UserRepository:
    def __init__(self, database=db):
        self.database = database

    @db.transaction
    def save(self, user) -> User:
        return user.save()

    @db.transaction
    def delete_user_by_id(self, id):
        user = User.nodes.get(uid=id)
        user.delete()

    @db.transaction
    def find_user_by_email(self, email):
        query = """
        MATCH (u:User) 
        WHERE u.email = $email AND u.provider IS NULL 
        RETURN u
        """
        results, meta = db.cypher_query(query, {"email": email})
        if results:
            user_node = results[0][0]
            user = User.inflate(user_node)
            return user
        return None

    @db.transaction
    def find_user_by_id(self, id) -> User:
        try:
            user = User.nodes.get(uid=id)
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
        parameters = {"username": username, "offset": offset, "limit": limit}
        results, _ = db.cypher_query(query, parameters)
        return [User.inflate(record[0]) for record in results]

    @db.transaction
    def get_all_users(self, offset: int, limit: int):
        query = "MATCH (u:User) RETURN u SKIP $offset LIMIT $limit"
        parameters = {"offset": offset, "limit": limit}
        results, _ = db.cypher_query(query, parameters)
        return [User.inflate(record[0]) for record in results]

    @db.transaction
    def get_following(self, id: str, offset: int, limit: int):
        query = "MATCH (u:User)-[:FOLLOW]->(f:User) WHERE u.uid = $id RETURN f SKIP $offset LIMIT $limit"
        parameters = {"id": id, "offset": offset, "limit": limit}
        results, _ = db.cypher_query(query, parameters)
        return [User.inflate(record[0]) for record in results]

    @db.transaction
    def get_followers(self, id: str, offset: int, limit: int):
        query = "MATCH (u:User)<-[:FOLLOW]-(f:User) WHERE u.uid = $id RETURN f SKIP $offset LIMIT $limit"
        parameters = {"id": id, "offset": offset, "limit": limit}
        results, _ = db.cypher_query(query, parameters)
        return [User.inflate(record[0]) for record in results]

    @db.transaction
    async def get_user_stats(self, uid: str, from_date):
        from_date_iso = from_date.isoformat()

        following_query = """
        MATCH (u:User)-[f:FOLLOW]->(o:User)
        WHERE u.uid = $uid AND f.created_at >= datetime($from_date).epochSeconds / 1000
        RETURN o
        """

        followers_query = """
        MATCH (o:User)-[f:FOLLOW]->(u:User)
        WHERE u.uid = $uid AND f.created_at >= datetime($from_date).epochSeconds / 1000
        RETURN o
        """

        followers_result, _ = db.cypher_query(
            followers_query, {"uid": uid, "from_date": from_date_iso}
        )
        logger.debug(f"Followers result: {followers_result}")
        following_result, _ = db.cypher_query(
            following_query, {"uid": uid, "from_date": from_date_iso}
        )
        logger.debug(f"Following result: {following_result}")

        followers_gained = len([User.inflate(record[0]) for record in followers_result])
        following_gained = len([User.inflate(record[0]) for record in following_result])

        return (followers_gained, following_gained)


user_repository = UserRepository()
