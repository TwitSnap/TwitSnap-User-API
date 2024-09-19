from models.user import User
from repositories.user_repository import user_repository
from DTOs.user_register import UserRegister
class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def create_user(self, register_request: UserRegister):
        new_user = User(username = register_request.username,
                        mail = register_request.mail,
                        phone = register_request.phone,)
        new_user = self.user_repository.create_user(new_user)
        return new_user
    
    async def get_user_id_by_mail(self, mail):
        user = self.user_repository.find_user_by_mail(mail)
        return user.uid
    
user_service = UserService(user_repository)