from typing import Union
from pydantic import BaseModel, ConfigDict

class TodoBase(BaseModel):
    title: str
    description: Union[str, None] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    title: Union[str, None] = None
    description: Union[str, None] = None
    completed: Union[bool, None] = None

class Todo(TodoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
