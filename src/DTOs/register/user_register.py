import pycountry
from pydantic import BaseModel, EmailStr, Field, field_validator
class UserRegister(BaseModel): 
    username: str = Field (min_length = 3, max_length = 20)  
    email: EmailStr
    password: str = Field (min_length = 8) 
    phone: str 
    country: str 

    @field_validator('country')
    def validate_country(cls, country):
        valid_countries = {country.alpha_2 for country in pycountry.countries}
        if country not in valid_countries:
            raise ValueError(f"invalid country: '{country}'.")
        return country

