from fastapi import FastAPI

from app.config import settings
from app.auth.router import router as auth_router
from app.questions.router import router as questions_router

app = FastAPI()

# Register routers
app.include_router(auth_router)
app.include_router(questions_router)

@app.get('/')
async def root():
    return {'message': f'Welcome to {settings.APP_NAME}'}

# temp
from app.models import User
from fastapi import Depends
from app.auth.dependencies import get_current_user
@app.get('/test')
async def test(user: User = Depends(get_current_user)):
    return {'message': 'Test endpoint'}
