from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.config import settings
from app.auth.router import router as auth_router
from app.questions.router import router as questions_router
from app.admin.router import router as admin_router

app = FastAPI()

# Register routers
app.include_router(auth_router)
app.include_router(questions_router)
app.include_router(admin_router)

# Add pagination
add_pagination(app)

# Root Endpoint
@app.get('/')
async def root():
    return {'message': f'Welcome to {settings.APP_NAME}'}