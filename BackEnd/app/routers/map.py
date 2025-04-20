from fastapi import APIRouter, HTTPException
from app.models.map import PathPlanRequest, PathPlanResponse
from app.services import map_service

router = APIRouter(prefix="/map", tags=["路径规划"])

@router.post("/path_plan", response_model=PathPlanResponse, summary="A* 算法路径规划")
def path_plan(map_req: PathPlanRequest):
    """
    A* 算法路径规划：
      - 根据请求参数调用 map_service.a_star 方法
      - 如果找不到路径，抛出 404 错误
    """
    distance, time, path = map_service.a_star(map_req.start, map_req.end, map_req.mode)
    if distance == float('inf'):
        raise HTTPException(status_code=404, detail="未能找到合适的路径")
    return PathPlanResponse(distance=distance, time=time, path=path)