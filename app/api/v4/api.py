from fastapi import APIRouter
from app.api.v4.endpoints import planets, stars

api_router = APIRouter()
api_router.include_router(planets.router, tags=["planets"])
api_router.include_router(stars.router, prefix="/stars", tags=["stars"])
