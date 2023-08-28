# Global models
from pydantic import BaseModel, EmailStr 

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_active: bool = True