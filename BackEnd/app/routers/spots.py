from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.spot_service import get_scenic_spots, get_schools
from app.models.spots import Spot

router = APIRouter(tags=["地点查询"])

@router.get("/scenic_spots/{name}", response_model=List[Spot], summary="查询特定地点并排序")
def query_scenic_spots(
    name: str,
    tag: str = Query(default="__all__", description="需要筛选的标签"),
    sort_key: str = Query(default="popularity", description="排序字段（rating/popularity）"),
    sort_order: str = Query(default="desc", description="排序方向：asc/desc")
):
    print(name)
    try:
        return get_scenic_spots(name, tag, sort_key, sort_order)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务器内部错误")

@router.get("/schools/{name}", response_model=List[Spot], summary="查询特定学校并排序")
def query_schools(
    name: str,
    tag: str = Query(default="__all__", description="需要筛选的标签"),
    sort_key: str = Query(default="popularity", description="排序字段（rating/popularity）"),
    sort_order: str = Query(default="desc", description="排序方向：asc/desc")
):
    print(name)
    try:
        return get_schools(name, tag, sort_key, sort_order)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务器内部错误")
