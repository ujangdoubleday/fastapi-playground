from fastapi import APIRouter
from app.api.v1.endpoints import items, root

api_router = APIRouter()

api_router.include_router(root.router, tags=["root"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
