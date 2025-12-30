from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas import item as item_schemas
from app.models import item as item_models

router = APIRouter()

@router.post("/", response_model=item_schemas.Item)
def create_item(item: item_schemas.ItemCreate, db: Session = Depends(deps.get_db)):
    db_item = item_models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model=item_schemas.Item)
def read_item(item_id: int, db: Session = Depends(deps.get_db)):
    db_item = db.query(item_models.Item).filter(item_models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.get("/", response_model=list[item_schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    items = db.query(item_models.Item).offset(skip).limit(limit).all()
    return items
