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
    def get_all_users(self, offset: int, limit: int, is_banned: bool = None):
        if is_banned is True:
            query = """
                MATCH (u:User)
                WHERE u.is_banned = true
                RETURN u SKIP $offset LIMIT $limit
            """
            count_query = """
                MATCH (u:User)
                WHERE u.is_banned = true
                RETURN count(u) AS total
            """
        elif is_banned is False:
            query = """
                MATCH (u:User)
                WHERE NOT u.is_banned
                RETURN u SKIP $offset LIMIT $limit
            """
            count_query = """
                MATCH (u:User)
                WHERE NOT u.is_banned
                RETURN count(u) AS total
            """
        else:
            query = """
                MATCH (u:User)
                RETURN u SKIP $offset LIMIT $limit
            """
            count_query = """
                MATCH (u:User)
                RETURN count(u) AS total
            """

        parameters = {"offset": offset, "limit": limit}
        results, _ = db.cypher_query(query, parameters)
        total_count, _ = db.cypher_query(count_query)

        users = [User.inflate(record[0]) for record in results]
        total = total_count[0][0]
        return users, total

    @db.transaction
    def get_following(self, id: str, offset: int, limit: int):
        query = "MATCH (u:User)-[:FOLLOW]->(f:User) WHERE u.uid = $id and f.is_banned = false RETURN f SKIP $offset LIMIT $limit"
        parameters = {"id": id, "offset": offset, "limit": limit}
        results, _ = db.cypher_query(query, parameters)
        return [User.inflate(record[0]) for record in results]

    @db.transaction
    def get_followers(self, id: str, offset: int, limit: int):
        query = "MATCH (u:User)<-[:FOLLOW]-(f:User) WHERE u.uid = $id and f.is_banned = false RETURN f SKIP $offset LIMIT $limit"
        parameters = {"id": id, "offset": offset, "limit": limit}
        results, _ = db.cypher_query(query, parameters)
        return [User.inflate(record[0]) for record in results]

    @db.transaction
    async def get_user_by_username(self, username: str):
        query = """
        MATCH (u:User)
        WHERE u.username = $username
        RETURN u
        """
        results, _ = db.cypher_query(query, {"username": username})
        if results:
            user_node = results[0][0]
            user = User.inflate(user_node)
            return user
        return None

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

        followers_gained = len([User.inflate(record[0]) for record in followers_result] )
        following_gained = len([User.inflate(record[0]) for record in following_result] )

        return (followers_gained, following_gained)

    async def get_metrics(self, metric_type: str):
        if metric_type == "register":
            return await self.get_register_metrics()
        elif metric_type == "banned":
            return await self.get_banned_metrics()
        elif metric_type == "country":
            return await self.get_country_metrics()

    async def get_register_metrics(self):
        query = """
        MATCH (u:User)
        WITH 
          COUNT(CASE WHEN u.provider IS NULL THEN u END) AS emailTotal,
          COUNT(CASE WHEN u.provider = 'google' THEN u END) AS googleTotal
        RETURN 
          emailTotal, 
          googleTotal
        """
        results, meta = db.cypher_query(query)
        return results[0]

    async def get_banned_metrics(self):
        query = """
        MATCH (u:User)
        WHERE u.is_banned = true
        RETURN u
        """
        results, meta = db.cypher_query(query)
        return len(results)

    async def get_country_metrics(self):
        query = """
        MATCH (u:User)
        WITH u.country AS country, COUNT(u) AS total
        RETURN country, total
        ORDER BY total DESC
        """
        results, meta = db.cypher_query(query)

        distribution = {row[0]: row[1] for row in results}
        return distribution


user_repository = UserRepository()
