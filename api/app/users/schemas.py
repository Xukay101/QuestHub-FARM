from typing import List
from datetime import datetime

from pydantic import BaseModel

from app.models import Question, Answer

class UserPublic(BaseModel):
    username: str
    created_at: datetime