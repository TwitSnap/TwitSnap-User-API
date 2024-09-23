from models.user import User
from repositories.user_repository import user_repository
from DTOs.register.user_register import UserRegister
class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def create_user(self, register_request: UserRegister):
        new_user = User(username = register_request.username,
                        email = register_request.email,
                        phone = register_request.phone,)
        return self.user_repository.create_user(new_user)
    
    async def create_user_with_federated_identity(self, id, email, username):
        new_user = User(username = username,
                        email = email,
                        uid = id,)
        return self.user_repository.create_user(new_user)
    
    async def get_user_id_by_email(self, mail):
        return  self.user_repository.find_user_by_email(mail).uid
    
    async def get_user_by_id(self, id):
        return self.user_repository.find_user_by_id(id)
    
    async def get_all_users(self):
        return self.user_repository.get_all_users()
    
user_service = UserService(user_repository)