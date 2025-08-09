from fastapi import APIRouter
from app.api import helper

api_router = APIRouter()


api_router.include_router(helper.router)