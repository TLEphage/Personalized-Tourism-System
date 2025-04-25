from fastapi import APIRouter, HTTPException
from app.models.map import PathPlanRequest, PathPlanResponse, NodeRequest, EdgeRequest
from app.services import map_service

router = APIRouter(tags=["路径规划"])

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

@router.get("/get_graph", summary="获取地图信息")
def get_graph():
    """获取地图信息"""
    return map_service.get_graph()

@router.post("/add_node", summary="添加地图节点")
def add_node(node: NodeRequest):
    """
    添加地图节点：
      - 接收节点信息
      - 验证节点ID唯一性
      - 追加到map.json数据文件
      - 返回新的图信息
    """
    info = map_service.add_node(node)
    if not info.get("success", False):
        raise HTTPException(status_code=404, detail="节点编号重复")
    return info.get("graph", {"nodes" : [] , "edges" : [] })

@router.post("/add_edge", summary="添加地图边")
def add_edge(edge: EdgeRequest):
    """
    添加地图边：
      - 接收边信息
      - 验证边ID和两端点唯一性
      - 追加到map.json数据文件
      - 返回新的图信息
    """
    info = map_service.add_edge(edge)
    if not info.get("success", False):
        raise HTTPException(status_code=404, detail="边信息不合法")
    return info.get("graph", {"nodes" : [] , "edges" : [] })