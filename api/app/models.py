# Global models
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    mail: str
    password: str