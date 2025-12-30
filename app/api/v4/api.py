from fastapi import APIRouter
from app.api.v4.endpoints import planets

api_router = APIRouter()
api_router.include_router(planets.router, tags=["planets"])
