from pydantic import BaseModel, Field
from typing import Optional, List, Dict,Any

class OneToOnePathRequest(BaseModel):
    """
    路径规划请求模型：
      - start: 起点名称
      - end: 终点名称
    """
    start: str
    end: str

class OneToOnePathResponse(BaseModel):
    path: list
    distance: float

class OneToOneTimeRequest(BaseModel):
    """
    路径规划请求模型：
        - start: 起点名称
        - end: 终点名称
        - mode: 交通方式
    """
    start: str
    end: str
    mode: str = "bike"

class OneToOneTimeResponse(BaseModel):
    path: list
    mode: list
    time: float
    distance: float

class OneToManyPathRequest(BaseModel):
    """
    路径规划请求模型：
        - start: 起点名称
        - end: 终点名称
    """
    start: str
    end: List[str]

class OneToManyPathResponse(BaseModel):
    path: list
    distance: float

class IndoorRequest(BaseModel):
    start: str
    end: str

class IndoorNode(BaseModel):
    id: int
    name: str
    type: str
    x: float
    y: float
    floor: int

class IndoorResponse(BaseModel):
    path: List[IndoorNode]
    distance: float

class NodeRequestRaw(BaseModel):
    nodeData: Dict[str, Any]

class NodeRequest(BaseModel):
    """地图数据节点模型"""
    id: Optional[int] = None
    name: str = "default"
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

class PlaceQueryRequest(BaseModel):
    """场所查询请求模型"""
    longitude: float    # 用户所在经度
    latitude: float     # 用户所在纬度
    query_type: str     # 要查询的场所类型（如："超市", "卫生间" 等）
    max_results: int = 100  # 最多返回结果数量，默认为100
    max_distance: float = 1000.0  # 最大范围，默认为1000m

class PlaceDetail(BaseModel):
    """场所详情响应模型"""
    id: int                 # 场所唯一标识
    name: str               # 场所名称
    type: str               # 场所类型（与查询类型对应）
    popularity: int         # 场所人气值
    longitude: float        # 场所经度
    latitude: float         # 场所纬度
    distance: float         # 距离用户的直线距离（单位：米）

class PlaceResponse(BaseModel):
    """场所查询响应模型"""
    places: List[PlaceDetail] = []