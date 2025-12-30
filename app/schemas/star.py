from typing import Optional

from pydantic import BaseModel

# Shared properties
class StarBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    galaxy: Optional[str] = None
    system: Optional[str] = None

# Properties to receive on star creation
class StarCreate(StarBase):
    name: str
    galaxy: str
    system: str

# Properties to receive on star update
class StarUpdate(StarBase):
    pass

# Properties shared by models stored in DB
class StarInDBBase(StarBase):
    id: int
    name: str
    galaxy: str
    system: str

    model_config = {"from_attributes": True}

# Properties to return to client
class Star(StarInDBBase):
    pass

# Properties properties stored in DB
class StarInDB(StarInDBBase):
    pass
