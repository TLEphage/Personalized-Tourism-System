import time, os
from app.config import DIARIES_FILE
from app.models.diaries import DiaryRequest, DiaryResponse, DiaryTagRequest
from utils.file_utils import read_json, write_json, read_compressed_json, write_compressed_json
from algorithm.Sort import quick_sort
from algorithm.TextSearch import kmp

# 在应用初始化时调用
if not os.path.exists(DIARIES_FILE):
    write_compressed_json(DIARIES_FILE, [])  # 写入空列表的压缩形式

def add_diary(
    username: str,
    title: str,
    content: str,
    images: list = None,
    videos: list = None,
    tags: list = None
):
    """
    添加日记：
    - 自动生成唯一id（当前最大id+1）
    - 初始化views为0，rating为0.0
    - 添加时间戳timestamp（保留原有功能）
    - 完整写入整个列表到文件
    """
    # 处理可变默认参数
    images = images or []
    videos = videos or []
    tags = tags or []

    # 读取现有日记并生成新ID
    diaries = read_compressed_json(DIARIES_FILE)
    max_id = max([entry.get("id", 0) for entry in diaries]) if diaries else 0
    new_id = max_id + 1

    # 创建完整日记条目
    diary_entry = {
        "username": username,
        "id": new_id,
        "title": title,
        "content": content,
        "images": images,
        "videos": videos,
        "views": 0,
        "rating": 5.0,
        "tags": tags,
        "timestamp": int(time.time())  # 保留原有时间戳功能
    }

    # 更新并写入完整列表
    diaries.append(diary_entry)
    write_compressed_json(DIARIES_FILE, diaries)
    return new_id

def get_diary(diary_id: int) -> dict:
    diaries = read_compressed_json(DIARIES_FILE)
    for entry in diaries:
        if(entry.get("id") == diary_id):
            entry["views"] += 1
            write_compressed_json(DIARIES_FILE, diaries)
            return {"message": "查找成功", "diary": entry}
    raise ValueError(f"未找到 ID 为 {diary_id} 的日记")

def get_user_diaries(username: str, sort_key: str = "id", sort_order: str = "desc") -> list:
    """
    根据用户名查询日记，支持自定义排序规则

    :param username: 查询用户名，"__all__"表示查询所有用户
    :param sort_key: 排序字段，默认按id排序
    :param sort_order: 排序方向，asc-升序 desc-降序（默认）
    :return: 过滤并排序后的日记列表
    """
    diaries = read_compressed_json(DIARIES_FILE)
    
    if username == "__all__":
        filtered = diaries
    else:
        filtered = [entry for entry in diaries if entry.get("username") == username]
    
    # 执行排序（使用带异常处理的排序方式）
    try:
        sorted_diaries = quick_sort(
            filtered,
            sort_key=lambda x: x.get(sort_key, 0),  # 为不存在的key提供默认值
            sort_order=sort_order
        )
    except TypeError:
        # 处理类型不一致的情况（如混合类型的字段），按原始顺序返回
        sorted_diaries = filtered
    
    return sorted_diaries

def search_diaries(title: str, content: str) -> list:
    diaries = read_compressed_json(DIARIES_FILE)
    
    if title == "__all__":
        filtered_by_title = diaries
    else:
        filtered_by_title = [entry for entry in diaries if entry.get("title") == title]

    if content == "__all__":
        filtered = diaries
    else:
        filtered = [entry for entry in filtered_by_title if kmp(entry.get("content"),content)]
    
    # 处理排序方向
    
    # 执行排序（使用带异常处理的排序方式）
    try:
        sorted_diaries = quick_sort(
            filtered,
            sort_key=lambda x: x.get("id", 0),  # 为不存在的key提供默认值
            sort_order="desc"
        )
    except TypeError:
        # 处理类型不一致的情况（如混合类型的字段），按原始顺序返回
        sorted_diaries = filtered
    
    return sorted_diaries

def update_diary(
    username: str,
    diary_id: int,
    fields: dict
) -> DiaryResponse:
    """
    更新日记：
    - 根据 username 和 id 查找日记条目
    - 如果不存在，抛出 ValueError
    - 更新传入的字段（title, content, images, videos, tags）
    - 保留其他字段（views, rating, timestamp）不变
    - 写回文件并返回更新后的日记对象
    """
    print(fields)
    diaries = read_compressed_json(DIARIES_FILE, default=[])
    # 查找目标日记
    for entry in diaries:
        if entry.get("id") == diary_id:
            # 更新可选字段，仅当不为 None 时才更新
            entry['username'] = username
            if fields.get("title") is not None:
                entry["title"] = fields["title"]
            if fields.get("content") is not None:
                entry["content"] = fields["content"]
            if fields.get("images") is not None:
                entry["images"] = fields["images"]
            if fields.get("videos") is not None:
                entry["video"] = fields["videos"]
            if fields.get("tags") is not None:
                entry["tags"] = fields["tags"]
            # 写回并返回
            write_compressed_json(DIARIES_FILE, diaries)
            return entry
    # 若未找到则抛出错误
    raise ValueError(f"未找到用户名 {username} 下 ID 为 {diary_id} 的日记")

def diary_append(
    diary_id: int,
    field: str,
    content: str
):
    diaries = read_compressed_json(DIARIES_FILE, default=[])
    # 查找目标日记
    for entry in diaries:
        if entry.get("id") == diary_id:
            if entry.get(field, None) is not None:
                entry[field].append(content)
            else:
                entry[field]=[content]
            write_compressed_json(DIARIES_FILE, diaries)
            return {"message": f"{field}成功添加{content}", "diary": entry}
    raise ValueError(f"未找到 ID 为 {diary_id} 的日记")

def rate_diary(
    diary_id: int,
    rate: float
):
    diaries = read_compressed_json(DIARIES_FILE, default=[])
    # 查找目标日记
    for entry in diaries:
        if entry.get("id") == diary_id:
            entry["rating"] = round((entry["rating"]*entry["views"]+rate)/(entry["views"]+1),2)
            write_compressed_json(DIARIES_FILE, diaries)
            return {"message": f"评分成功", "diary": entry}
    raise ValueError(f"未找到 ID 为 {diary_id} 的日记")
