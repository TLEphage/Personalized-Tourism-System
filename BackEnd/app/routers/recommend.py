from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.recommend_service import recommend_for_user
from app.models.recommend import RecommendResponse

router = APIRouter(tags=["地点查询"])

@router.get("/{username}", response_model=RecommendResponse, summary="为用户进行内容推荐")
def recommend(username: str):
    result = recommend_for_user(username)
    return result