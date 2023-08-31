# Global models
from typing import List
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True

class Question(BaseModel):
    title: str
    content: str
    votes: int
    tags: List[str]
    author_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = None
    is_archived: bool = False

class Tag(BaseModel):
    name: str
    description: str
    related_questions: List[str]

class Answer(BaseModel):
    content: str
    question_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = None