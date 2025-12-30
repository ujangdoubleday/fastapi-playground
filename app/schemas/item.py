from typing import Union
from pydantic import BaseModel, ConfigDict

class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None
    price: float
    is_offer: Union[bool, None] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
