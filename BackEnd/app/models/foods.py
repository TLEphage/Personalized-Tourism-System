from pydantic import BaseModel
from typing import Optional, List

class FoodResponse(BaseModel):
    restaurant_name: str
    description: str
    address: str
    latitude: float
    longitude: float
    popularity: int
    rating: float
    tags: List[str]

class FoodSearchRequest(BaseModel):
    latitude: float
    longitude: float
    search_text: Optional[str] = None
    tag: Optional[List[str]] = None
    sort_key: Optional[str] = None