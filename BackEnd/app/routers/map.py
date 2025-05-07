from fastapi import APIRouter, HTTPException
from app.models.map import *
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
def add_node(node: NodeRequestRaw):
    """
    添加地图节点：
      - 接收节点信息
      - 验证节点ID唯一性
      - 追加到map.json数据文件
      - 返回新的图信息
    """
    print(node)
    node_data = NodeRequest(**node.nodeData)
    info = map_service.add_node(node_data)
    if not info.get("success", False):
        raise HTTPException(status_code=404, detail="节点编号重复")
    return info.get("graph", {"nodes" : [] , "edges" : [] })

@router.post("/add_edge", summary="添加地图边")
def add_edge(edge: EdgeRequestRaw):
    """
    添加地图边：
      - 接收边信息
      - 验证边ID和两端点唯一性
      - 追加到map.json数据文件
      - 返回新的图信息
    """

    print(edge)
    edge_data = EdgeRequest(**edge.edgeDataToSend)
    info = map_service.add_edge(edge_data)
    if not info.get("success", False):
        raise HTTPException(status_code=404, detail="边信息不合法")
    return info.get("graph", {"nodes" : [] , "edges" : [] })

@router.post("/search_places", response_model=PlaceResponse, summary="查询最近场所")
def search_places(query: PlaceQueryRequest):
    """
    场所查询服务：
      - 根据用户坐标和场所类型进行搜索
      - 返回按距离排序的场所列表（由近到远）
      - 当没有匹配类型场所时，返回404错误
    """
    # 调用服务层获取查询结果
    found_places = map_service.search_places(
        longitude=query.longitude,
        latitude=query.latitude,
        query_type=query.query_type,
        max_results=query.max_results
    )

    # 处理无结果情况
    if not found_places:
        raise HTTPException(
            status_code=404,
            detail=f"未找到类型为 {query.query_type} 的场所"
        )

    return PlaceResponse(places=found_places)