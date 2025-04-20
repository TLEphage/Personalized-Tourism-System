from pydantic import BaseModel
from typing import List

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class OpenHours(BaseModel):
    weekday: str
    weekend: str

class Spot(BaseModel):
    name: str
    description: str
    location: str
    coordinates: Coordinates
    rating: float
    popularity: int
    tags: List[str]
    price_range: str
    open_hours: OpenHours