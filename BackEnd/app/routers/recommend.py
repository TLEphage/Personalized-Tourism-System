from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.recommend_service import recommend_for_user
from app.models.recommend import RecommendResponse

router = APIRouter(tags=["内容推荐"])

@router.get("/{username}", response_model=RecommendResponse, summary="为用户进行内容推荐")
def recommend(username: str):
    try:
        result = recommend_for_user(username)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))