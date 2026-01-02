from fastapi import APIRouter
from app.api.v4.endpoints import planets, stars, ws

api_router = APIRouter()
api_router.include_router(planets.router, tags=["planets"])
api_router.include_router(stars.router, prefix="/stars", tags=["stars"])
api_router.include_router(ws.router, tags=["websocket"])
