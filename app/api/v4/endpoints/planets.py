from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import planet as planet_schema
from app.models import planet as planet_model
from app.api import deps

router = APIRouter()

@router.get("/{galaxy}/{system}/{planet}", response_model=planet_schema.Planet)
def read_planet(
    galaxy: str,
    system: str,
    planet: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get planet by galaxy, system, and planet.
    """
    db_planet = db.query(planet_model.Planet).filter(
        planet_model.Planet.galaxy == galaxy,
        planet_model.Planet.system == system,
        planet_model.Planet.planet == planet
    ).first()
    if not db_planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    return db_planet

@router.post("/{galaxy}/{system}/{planet}", response_model=planet_schema.Planet)
def create_planet(
    galaxy: str,
    system: str,
    planet: str,
    planet_in: planet_schema.PlanetCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create new planet.
    """
    db_planet = db.query(planet_model.Planet).filter(
        planet_model.Planet.galaxy == galaxy,
        planet_model.Planet.system == system,
        planet_model.Planet.planet == planet
    ).first()
    if db_planet:
        # idempotency / conflict check
        raise HTTPException(status_code=400, detail="Planet already exists")

    db_planet = planet_model.Planet(
        **planet_in.model_dump(),
        galaxy=galaxy,
        system=system,
        planet=planet
    )
    db.add(db_planet)
    db.commit()
    db.refresh(db_planet)
    return db_planet

@router.put("/{galaxy}/{system}/{planet}", response_model=planet_schema.Planet)
def update_planet(
    galaxy: str,
    system: str,
    planet: str,
    planet_in: planet_schema.PlanetUpdate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Update a planet.
    """
    db_planet = db.query(planet_model.Planet).filter(
        planet_model.Planet.galaxy == galaxy,
        planet_model.Planet.system == system,
        planet_model.Planet.planet == planet
    ).first()
    if not db_planet:
        raise HTTPException(status_code=404, detail="Planet not found")

    update_data = planet_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_planet, field, value)

    db.add(db_planet)
    db.commit()
    db.refresh(db_planet)
    return db_planet

@router.delete("/{galaxy}/{system}/{planet}", response_model=planet_schema.Planet)
def delete_planet(
    galaxy: str,
    system: str,
    planet: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Delete a planet.
    """
    db_planet = db.query(planet_model.Planet).filter(
        planet_model.Planet.galaxy == galaxy,
        planet_model.Planet.system == system,
        planet_model.Planet.planet == planet
    ).first()
    if not db_planet:
        raise HTTPException(status_code=404, detail="Planet not found")

    db.delete(db_planet)
    db.commit()
    return db_planet
