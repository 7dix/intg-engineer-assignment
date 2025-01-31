from pydantic import BaseModel, field_validator
import re
import uuid
import os

"""
Model for the customer data with validation.

Raises:
    ValueError: One of the fields is invalid.
"""
class CustomerData(BaseModel):
    Name: str
    Age: int
    Cookie: str
    BannerId: int
    
    @field_validator('Name')
    def validate_name(cls, value):
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise ValueError('Name must only contain letters and spaces.')
        return value
    
    @field_validator('Age')
    def validate_age(cls, value):
        min_age = int(os.getenv('MIN_AGE'))
        max_age = int(os.getenv('MAX_AGE'))
        
        if not max_age or not min_age:
            raise ValueError('Age range not set in .env file.')
        if value <= min_age or value >= max_age:
            raise ValueError(f'Age must be between {min_age} and {max_age}.')
        return value
    
    @field_validator('Cookie')
    def validate_cookie(cls, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError('Cookie must be a valid UUID.')
        return value
    
    @field_validator('BannerId')
    def validate_banner(cls, value):
        if 0 > value or value > 100:
            raise ValueError('Banner ID must be between 0 and 100.')
        return value
    