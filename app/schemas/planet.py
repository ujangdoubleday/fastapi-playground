from typing import Optional
from pydantic import BaseModel, ConfigDict

class PlanetBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class PlanetCreate(PlanetBase):
    name: str

class PlanetUpdate(PlanetBase):
    pass

class Planet(PlanetBase):
    id: int
    galaxy: str
    system: str
    planet: str

    model_config = ConfigDict(from_attributes=True)
