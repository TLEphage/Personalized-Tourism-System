from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models.foods import *
from app.services import food_service

router = APIRouter(tags=["美食搜索"])

@router.post("/search", response_model=List[FoodResponse], summary="美食搜索")
async def search_foods(request: FoodSearchRequest):
    """
    美食搜索接口：
      - 可以按照用户选择的热度、评价和距离进行排序，并根据菜系进行过滤
      - 输入美食名称、菜系、饭店或窗口 名称等进行基于内容的模糊查询
    """
    return food_service.search_foods(
        latitude=request.latitude,
        longitude=request.longitude,
        search_text=request.search_text,
        tag=request.tag,
        sort_key=request.sort_key
    )