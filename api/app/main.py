from fastapi import FastAPI

from app.config import settings

app = FastAPI()

@app.get('/')
def root():
    return {'message': f'Welcome to {settings.app_name}'}

@app.get('/test')
def test():
    return settings.model_dump()