from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app.models import item as item_models
from app.schemas import item as item_schemas

router = APIRouter()

# --- Helpers ---
def item_to_xml(item) -> str:
    # Basic XML serialization
    return f"""<Item>
    <ID>{item.id}</ID>
    <Title>{item.title}</Title>
    <Description>{item.description or ''}</Description>
    <Price>{item.price}</Price>
    <IsOffer>{str(item.is_offer).lower()}</IsOffer>
</Item>"""

def items_to_xml(items) -> str:
    content = "".join([item_to_xml(i) for i in items])
    return f"<?xml version='1.0'?><Items>{content}</Items>"

# --- JSON Endpoints ---

@router.post("/json/items/", response_class=JSONResponse)
def create_item_json(item: item_schemas.ItemCreate, db: Session = Depends(deps.get_db)):
    db_item = item_models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    # Direct JSONResponse return
    return JSONResponse(content=jsonable_encoder(db_item), status_code=201)

@router.get("/json/items/", response_class=JSONResponse)
def read_items_json(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    items = db.query(item_models.Item).offset(skip).limit(limit).all()
    return JSONResponse(content=jsonable_encoder(items))

@router.get("/json/items/{item_id}", response_class=JSONResponse)
def read_item_json(item_id: int, db: Session = Depends(deps.get_db)):
    db_item = db.query(item_models.Item).filter(item_models.Item.id == item_id).first()
    if db_item is None:
        return JSONResponse(content={"error": "Item not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(db_item))

@router.put("/json/items/{item_id}", response_class=JSONResponse)
def update_item_json(item_id: int, item: item_schemas.ItemCreate, db: Session = Depends(deps.get_db)):
    db_item = db.query(item_models.Item).filter(item_models.Item.id == item_id).first()
    if db_item is None:
        return JSONResponse(content={"error": "Item not found"}, status_code=404)
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return JSONResponse(content=jsonable_encoder(db_item))

@router.delete("/json/items/{item_id}", response_class=JSONResponse)
def delete_item_json(item_id: int, db: Session = Depends(deps.get_db)):
    db_item = db.query(item_models.Item).filter(item_models.Item.id == item_id).first()
    if db_item is None:
        return JSONResponse(content={"error": "Item not found"}, status_code=404)
    db.delete(db_item)
    db.commit()
    return JSONResponse(content={"message": "Item deleted successfully"})


# --- XML Endpoints ---

@router.post("/xml/items/")
def create_item_xml(item: item_schemas.ItemCreate, db: Session = Depends(deps.get_db)):
    db_item = item_models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    # Direct Custom Response Return
    return Response(content=item_to_xml(db_item), media_type="application/xml", status_code=201)

@router.get("/xml/items/")
def read_items_xml(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    items = db.query(item_models.Item).offset(skip).limit(limit).all()
    return Response(content=items_to_xml(items), media_type="application/xml")

@router.get("/xml/items/{item_id}")
def read_item_xml(item_id: int, db: Session = Depends(deps.get_db)):
    db_item = db.query(item_models.Item).filter(item_models.Item.id == item_id).first()
    if db_item is None:
        return Response(content="<Error>Item not found</Error>", media_type="application/xml", status_code=404)
    return Response(content=item_to_xml(db_item), media_type="application/xml")

@router.put("/xml/items/{item_id}")
def update_item_xml(item_id: int, item: item_schemas.ItemCreate, db: Session = Depends(deps.get_db)):
    db_item = db.query(item_models.Item).filter(item_models.Item.id == item_id).first()
    if db_item is None:
        return Response(content="<Error>Item not found</Error>", media_type="application/xml", status_code=404)
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return Response(content=item_to_xml(db_item), media_type="application/xml")

@router.delete("/xml/items/{item_id}")
def delete_item_xml(item_id: int, db: Session = Depends(deps.get_db)):
    db_item = db.query(item_models.Item).filter(item_models.Item.id == item_id).first()
    if db_item is None:
        return Response(content="<Error>Item not found</Error>", media_type="application/xml", status_code=404)
    db.delete(db_item)
    db.commit()
    return Response(content="<Message>Item deleted successfully</Message>", media_type="application/xml")
