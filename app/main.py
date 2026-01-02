from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.api.v2.api import api_router as api_router_v2
from app.api.v3.api import api_router as api_router_v3
from app.api.v4.api import api_router as api_router_v4
from app.db.base import Base
from app.db.session import engine
from app.models import item, todo
from app.models import user  # noqa


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router_v2, prefix="/api/v2")
app.include_router(api_router_v3, prefix="/api/v3")
app.include_router(api_router_v4, prefix="/api/v4")