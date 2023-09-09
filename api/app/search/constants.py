from enum import Enum

class ModelEnum(str, Enum):
    QUESTION = "question"
    ANSWER = "answer"
    USER = "user"
    TAG = "tag"