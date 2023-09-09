from pydantic import BaseModel

from app.search.constants import ModelEnum

class SearchResultItem(BaseModel):
    type: ModelEnum
    data: dict