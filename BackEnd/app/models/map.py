from pydantic import BaseModel
from typing import Optional, List

class PathPlanRequest(BaseModel):
    """
    路径规划请求模型：
      - start: 起点名称
      - end: 终点名称
      - mode: 规划模式（0: 最短路径，1: 步行最短时间，2: 自行车最短时间，3: 电动车最短时间）
    """
    start: str
    end: str
    mode: int

class PathPlanResponse(BaseModel):
    """
    路径规划响应模型：
      - distance: 距离（米）
      - time: 时间（秒）
      - path: 路径节点列表
    """
    distance: float
    time: float
    path: list

class NodeRequest(BaseModel):
    """地图数据节点模型"""
    id: Optional[int] = None
    name: str
    type: Optional[str] = "default"
    popularity: Optional[int] = 100
    longitude: float    # 经度
    latitude: float     # 纬度
    connected_edges: Optional[List[int]] = None

class EdgeRequest(BaseModel):
    """地图数据边模型"""
    id: Optional[int] = None
    start_node: int
    end_node: int
    distance: Optional[int] = None
    walk_speed: Optional[float] = 1.0
    bike_speed: Optional[float] = 0.0
    ebike_speed: Optional[float] = 0.0