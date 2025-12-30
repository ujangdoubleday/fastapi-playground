from fastapi import APIRouter, Depends
from app.api import deps
from app.models import user as user_model

router = APIRouter()

@router.get("/")
def read_hello(current_user: user_model.User = Depends(deps.get_current_user)):
    return {"message": "Hello World", "user": current_user.email}
