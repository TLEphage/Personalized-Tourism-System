import math
from typing import List, Optional
from app.models.foods import FoodResponse
from app.config import FOODS_FILE
from utils.file_utils import read_json

# 全局变量存储美食数据
foods_list = None

def _load_foods_data():
    """加载景点数据到内存"""
    global foods_list
    if foods_list is not None:
        return
    foods_dict = read_json(FOODS_FILE, default={})
    foods_list = foods_dict.get("foods",[])

# 服务启动时加载数据
_load_foods_data()

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """计算两个经纬度坐标之间的距离（公里）"""
    R = 6371000  # 地球半径（米）
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2) * math.sin(dlat/2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon/2) * math.sin(dlon/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def search_foods(
    latitude: float,
    longitude: float,
    search_text: Optional[str] = None,
    tag: Optional[str] = None,
    sort_key: Optional[str] = None
) -> List[FoodResponse]:
    
    # 初步筛选
    filtered = foods_list
    
    # 名称筛选
    if search_text:
        search_lower = search_text.lower()
        filtered = [f for f in filtered if search_lower in f["restaurant_name"].lower()]
    
    # 标签筛选
    if tag:
        filtered = [f for f in filtered if tag in f["tags"]]
    
    # 排序逻辑

    # valid_fields = ["distance", "rating", "popularity"]
    # if sort_key is None or sort_key not in valid_fields:
    #     sort_key = "distance"
    reverse = sort_key in ["popularity", "rating"]  # 这些字段降序排列
    
    def get_sort_value(food):
        if sort_key == "distance":
            return haversine(latitude, longitude, food["latitude"], food["longitude"])
        return food[sort_key]
    
    sorted_foods = sorted(filtered, key=get_sort_value, reverse=reverse)
    
    # 转换为响应模型
    return [FoodResponse(**food) for food in sorted_foods]