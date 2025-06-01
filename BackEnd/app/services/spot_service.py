from typing import List
from app.models.spots import Spot
from app.config import SPOTS_FILE
from utils.file_utils import read_json
from algorithm.Sort import partial_selection_sort

# 全局变量存储景点数据
scenic_spot_list = None
school_list = None

def _load_spots_data():
    """加载景点数据到内存"""
    global scenic_spot_list
    global school_list
    spots_dict = read_json(SPOTS_FILE, default={})
    scenic_spot_list = spots_dict.get("scenic_spots",[])
    school_list = spots_dict.get("schools",[])

# 服务启动时加载数据
_load_spots_data()

def get_scenic_spots(name: str = "__all__", tag: str = "__all__", sort_key: str = "popularity", sort_order: str = "desc") -> List[Spot]:
    """根据名称查询景点"""
    valid_fields = ["rating", "popularity"]
    if sort_key not in valid_fields:
        raise ValueError(f"无效排序字段，允许值：{valid_fields}")
    
    if name == "__all__":
        filtered_by_name = scenic_spot_list
    else:
        filtered_by_name = [spot for spot in scenic_spot_list if name in spot.get('name','')]

    if tag == "__all__":
        filtered = filtered_by_name
    else:
        filtered = [spot for spot in filtered_by_name if any(tag in t for t in spot.get('tags', []))]

    if not filtered:
        raise ValueError("景点不存在")
    try:
        sorted_spots = partial_selection_sort(
            filtered,
            sort_key=lambda x: x.get(sort_key, 0),  # 为不存在的key提供默认值
            sort_order=sort_order
        )
    except TypeError:
        # 处理类型不一致的情况（如混合类型的字段），按原始顺序返回
        sorted_spots = filtered

    return sorted_spots

def get_schools(name: str = "__all__", tag: str = "__all__", sort_key: str = "popularity", sort_order: str = "desc") -> List[Spot]:
    """根据名称查询景点"""
    valid_fields = ["rating", "popularity"]
    if sort_key not in valid_fields:
        raise ValueError(f"无效排序字段，允许值：{valid_fields}")
    if name == "__all__":
        filtered_by_name = school_list
    else:
        filtered_by_name = [spot for spot in school_list if name in spot.get('name','')]
    
    if tag == "__all__":
        filtered = filtered_by_name
    else:
        filtered = [spot for spot in filtered_by_name if any(tag in t for t in spot.get('tags', []))]

    if not filtered:
        raise ValueError("景点不存在")
    try:
        sorted_spots = partial_selection_sort(
            filtered,
            sort_key=lambda x: x.get(sort_key, 0),  # 为不存在的key提供默认值
            sort_order=sort_order
        )
    except TypeError:
        # 处理类型不一致的情况（如混合类型的字段），按原始顺序返回
        sorted_spots = filtered

    return sorted_spots
