from typing import Optional

from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name:str
    color: Optional[str] = None

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None

class TagResponse(TagBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
