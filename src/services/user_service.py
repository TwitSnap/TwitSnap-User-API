from models.user import User
from repositories.user_repository import user_repository
from DTOs.register.user_register import UserRegister
from exceptions.resource_not_found_exception import ResourceNotFoundException
from exceptions.conflict_exception import ConflictException 
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
    
    async def get_user_id_by_email(self, email):
        user = self.user_repository.find_user_by_email(email)
        if user is None:
            raise ResourceNotFoundException(detail=f"User not found with email: {email}")
        return user.uid
    
    async def get_user_by_id(self, id):
        user = self.user_repository.find_user_by_id(id)
        if user is None:
            raise ResourceNotFoundException(detail=f"User not found with id: {id}")
        return user
    
    async def exists_user_by_email(self, email):
        return self.user_repository.find_user_by_email(email) is not None
           
    async def get_all_users(self):
        return self.user_repository.get_all_users()
    
user_service = UserService(user_repository)