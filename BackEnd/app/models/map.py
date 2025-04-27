from pydantic import BaseModel, Field
from typing import Optional, List, Dict,Any

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

class NodeRequestRaw(BaseModel):
    nodeData: Dict[str, Any]

class NodeRequest(BaseModel):
    """地图数据节点模型"""
    id: Optional[int] = None
    name: str
    type: str = "default"
    popularity: int = 100
    longitude: float    # 经度
    latitude: float     # 纬度
    connected_edges: List[int] = []

class EdgeRequestRaw(BaseModel):
    edgeDataToSend: Dict[str, Any]

class EdgeRequest(BaseModel):
    """地图数据边模型"""
    id: Optional[int] = Field(default=None, description="边ID，为空时自动生成")
    start_node: int = Field(..., description="起始节点ID（必填）")
    end_node: int = Field(..., description="目标节点ID（必填）")
    distance: Optional[int] = Field(default=None, description="手动设置距离（米）")
    walk_speed: Optional[float] = Field(default=1.0, ge=0, le=5, description="步行速度 m/s")
    bike_speed: Optional[float] = Field(default=0.0, ge=0, le=10, description="自行车速度 m/s")
    ebike_speed: Optional[float] = Field(default=0.0, ge=0, le=15, description="电动车速度 m/s")