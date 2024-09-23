from pydantic import BaseModel, EmailStr, Field
class UserRegister(BaseModel):
    register_type: str = Field (pattern ='^(email|google)$')  
    username: str = Field (min_length = 3, max_length = 20)  
    email: EmailStr
    password: str = Field (min_length = 8) 
    phone: str 
    country: str 

