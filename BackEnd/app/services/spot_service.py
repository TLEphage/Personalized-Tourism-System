from typing import List
from app.models.spots import Spot
from app.config import DIARIES_FILE
from utils.file_utils import read_json

# 全局变量存储景点数据
spots_data = None

def _load_spots_data():
    """加载景点数据到内存"""
    global spots_data
    if spots_data is not None:
        return
    spots_data = read_json(DIARIES_FILE, default={})

# 服务启动时加载数据
_load_spots_data()

def get_spot_by_name(name: str) -> Spot:
    """根据名称查询景点"""
    for spot in spots_data:
        if spot.name == name:
            return spot
    raise ValueError("景点不存在")

def get_sorted_spots(sort_key: str, reverse: bool) -> List[Spot]:
    """获取排序后的景点列表"""
    valid_fields = ["rating", "popularity"]
    if sort_key not in valid_fields:
        raise ValueError(f"无效排序字段，允许值：{valid_fields}")
    
    return sorted(
        spots_data,
        key=lambda x: getattr(x, sort_key),
        reverse=reverse
    )

def get_spots_by_tag(tag: str) -> List[Spot]:
    """根据标签筛选景点"""
    filtered = [spot for spot in spots_data if tag in spot.tags]
    if not filtered:
        raise ValueError("未找到匹配标签的景点")
    return filtered