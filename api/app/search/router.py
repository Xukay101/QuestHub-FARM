from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate

from app.database import TagController, UserController, QuestionController
from app.search.schemas import SearchResultItem
from app.search.constants import ModelEnum

router = APIRouter(
    prefix='/search', 
    tags=['search'], 
    responses={404: {"description": "Not found"}}
)

@router.get('/', status_code=200, response_model=Page[SearchResultItem])
async def search(q: str | None = None, tag: str | None = None, user: str | None = None):
    init_args = {'q': q, 'tag': tag, 'user': user}

    final_args = {k:v for k, v in init_args.items() if v}
    if not final_args:
        raise HTTPException(400, 'You must provide at least one search argument')

    results = []

    if tag:
        tag_dict = await TagController.get_by_name(tag)
        del tag_dict['_id']
        if tag_dict:
            results.append(SearchResultItem(type=ModelEnum.TAG, data=tag_dict))

    questions = await QuestionController.search_by_args(**final_args)
    results.extend([
        SearchResultItem(type=ModelEnum.QUESTION, data=question.model_dump())
    for question in questions])

    return paginate(results)