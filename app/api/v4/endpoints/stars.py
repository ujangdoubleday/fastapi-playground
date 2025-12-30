from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import star as star_schema
from app.models import star as star_model
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[star_schema.Star])
def read_stars(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve stars.
    """
    stars = db.query(star_model.Star).offset(skip).limit(limit).all()
    return stars

@router.post("/", response_model=star_schema.Star)
def create_star(
    *,
    db: Session = Depends(deps.get_db),
    star_in: star_schema.StarCreate,
) -> Any:
    """
    Create new star.
    """
    star = star_model.Star(
        name=star_in.name,
        description=star_in.description,
        galaxy=star_in.galaxy,
        system=star_in.system,
    )
    db.add(star)
    db.commit()
    db.refresh(star)
    return star

@router.get("/{id}", response_model=star_schema.Star)
def read_star(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get star by ID.
    """
    star = db.query(star_model.Star).filter(star_model.Star.id == id).first()
    if not star:
        raise HTTPException(status_code=404, detail="Star not found")
    return star

@router.put("/{id}", response_model=star_schema.Star)
def update_star(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    star_in: star_schema.StarUpdate,
) -> Any:
    """
    Update a star.
    """
    star = db.query(star_model.Star).filter(star_model.Star.id == id).first()
    if not star:
        raise HTTPException(status_code=404, detail="Star not found")
    
    update_data = star_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(star, field, value)
    
    db.add(star)
    db.commit()
    db.refresh(star)
    return star

@router.delete("/{id}", response_model=star_schema.Star)
def delete_star(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete a star.
    """
    star = db.query(star_model.Star).filter(star_model.Star.id == id).first()
    if not star:
        raise HTTPException(status_code=404, detail="Star not found")
    
    db.delete(star)
    db.commit()
    return star
