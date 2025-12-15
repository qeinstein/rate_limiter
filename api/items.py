from fastapi import APIRouter, HTTPException, status, Header, Depends
from typing import List
from uuid import uuid4
from datetime import datetime, timezone

from rate_limiter.models.item import ItemCreate, Item
from rate_limiter.core.metrics_store import get_global_metrics_store


router = APIRouter()

#in memory store, to avoid db issues
_items = []

@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item_in: ItemCreate):
    if not item_in.name or item_in.price <= 0: #checking for invalid fields
        raise HttpException(
            status_code=400,
            detail="Invalid input"
        ) 
    
    item = Item(
        id=str(uuid4()),
        name=item_in.name,
        price=item_in.price,
        created_at=datetime.now(tz=timezone.utc).isoformat(),
    )
    _items.append(item.model_dump())  #normal adding to dictionary
    return item

@router.get("/items", response_model=List[Item])
async def list_items():
    #return each item in the dict
    return [Item(**i) for i in _items]


