import pycountry
from pydantic import BaseModel, Field, field_validator
from typing import Optional

from config.settings import INTERESTS


class EditUser(BaseModel):
    username: Optional[str] = Field(min_length=3, max_length=20)
    phone: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    interests: Optional[list[str]] = None

    @field_validator("country")
    def validate_country(cls, country):
        if country is None:
            return country

        valid_countries = {country.alpha_2 for country in pycountry.countries}
        if country not in valid_countries:
            raise ValueError(f"invalid country: '{country}'.")
        return country

    @field_validator("interests")
    def validate_interests(cls, interests):
        if interests is None:
            return interests

        for interest in interests:
            if not interest:
                return []
            if interest.lower() not in INTERESTS:
                raise ValueError(
                    f"Invalid interest: '{interest}', valid values: {INTERESTS}"
                )

        return interests