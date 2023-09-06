# Global models
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: str | None = None
    username: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True

class Question(BaseModel):
    id: str | None = None
    title: str | None = None
    content: str | None = None
    tag: str | None = None
    votes: dict = {}
    author_id: str = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    is_archived: bool = False

class Tag(BaseModel):
    id: str | None = None
    name: str
    description: str
    created_at: datetime = Field(default_factory=datetime.now)

class Answer(BaseModel):
    id: str | None = None
    content: str | None = None
    question_id: str | None = None
    author_id: str | None = None
    votes: dict = {}
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None

class Admin(BaseModel):
    id: str | None = None
    username: str
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    level: int = 1
    is_active: bool = True
