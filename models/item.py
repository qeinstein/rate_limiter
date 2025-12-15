#supposed to create a schema for each item
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=3) #at least 3chars faa
    price: float = Field(..., gt=0)

class Item(BaseModel):
    id: str
    name: str
    price: float
    created_at: str
    