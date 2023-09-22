from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

from app.config import settings
from app.auth.router import router as auth_router
from app.questions.router import router as questions_router
from app.admin.router import router as admin_router
from app.answers.router import router as answers_router
from app.tags.router import router as tags_router 
from app.users.router import router as users_router
from app.search.router import router as search_router 

app = FastAPI()

# Add Middleware
app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.CLIENT_URL],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
)

# Register routers
app.include_router(auth_router)
app.include_router(questions_router)
app.include_router(admin_router)
app.include_router(answers_router)
app.include_router(tags_router)
app.include_router(users_router)
app.include_router(search_router)

# Add pagination
add_pagination(app)
disable_installed_extensions_check()

# Root Endpoint
@app.get('/')
async def root():
    return {'message': f'Welcome to {settings.APP_NAME}'}
