from models.user import User
from repositories.user_repository import user_repository
from DTOs.user_register import UserRegistration
class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def create_user(self, register_request: UserRegistration):
        new_user = User(username = register_request.username,
                        mail = register_request.mail,
                        phone = register_request.phone,)
        new_user = self.user_repository.create_user(new_user)
        return (new_user.uid,register_request.password) #

user_service = UserService(user_repository)