from fastapi import APIRouter
from frcm.API.routes import delta, period, timedelta

api_router = APIRouter()
api_router.include_router(period.router, prefix="", tags=["period"])
api_router.include_router(timedelta.router, prefix="", tags=["timedelta"])
api_router.include_router(delta.router, prefix="", tags=["delta"])