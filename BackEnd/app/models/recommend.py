from pydantic import BaseModel
from typing import Optional, List

class RecommendItem(BaseModel):
    item: dict
    match_score: float
    final_score: float

class RecommendResponse(BaseModel):
    schools: List[RecommendItem]
    scenic_spots: List[RecommendItem]
    foods: List[RecommendItem]
    diaries: List[RecommendItem]