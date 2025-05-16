from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.spot_service import (
    get_spot_by_name,
    get_spots_by_tag
)
from app.models.spots import Spot

router = APIRouter(tags=["景点查询"])

@router.get("/{name}", response_model=List[Spot], summary="查询特定景点并排序")
def query_spot(
    name: str,
    sort_key: str = Query(default="popularity", description="排序字段（rating/popularity）"),
    sort_order: str = Query(default="desc", description="排序方向：asc/desc")
):
    print(name)
    try:
        return get_spot_by_name(name, sort_key, sort_order)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务器内部错误")

# @router.get("/", response_model=List[Spot], summary="排序景点列表")
# def sort_spots(
#     sort_key: str = Query(default="popularity", description="排序字段（rating/popularity）"),
#     sort_order: str = Query(default="desc", description="排序方向：asc/desc")
# ):
#     try:
#         reverse = sort_order.lower() == "desc"
#         return get_sorted_spots(sort_key=sort_key, reverse=reverse)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="服务器内部错误")

@router.get("/tag/", response_model=List[Spot], summary="按标签筛选")
def filter_by_tag(tag: str = Query(..., description="需要筛选的标签")):
    try:
        return get_spots_by_tag(tag)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务器内部错误")