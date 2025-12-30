from typing import Union
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None
    price: float
    is_offer: Union[bool, None] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True
