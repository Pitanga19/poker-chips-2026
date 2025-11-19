from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings as sett
from app.db import base

app = FastAPI(title=sett.PROJECT_NAME, version=sett.PROJECT_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/', tags=['Home'])
def root():
    return {'msg': 'Hola poker'}
