from fastapi import FastAPI

from app.config import settings
from app.auth.router import router as auth_router

app = FastAPI()

# Register routers
app.include_router(auth_router)

@app.get('/')
async def root():
    return {'message': f'Welcome to {settings.APP_NAME}'}