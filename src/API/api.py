from fastapi import APIRouter
from API.routes import get_fr

api_router = APIRouter()
api_router.include_router(get_fr.router, prefix="", tags=["get_fr"])