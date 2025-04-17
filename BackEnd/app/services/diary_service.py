import time
from app.config import DIARIES_FILE
from utils.file_utils import read_json, write_json

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
    diaries = read_json(DIARIES_FILE, default=[])
    max_id = max((entry.get("id", 0) for entry in diaries) if diaries else 0)
    new_id = max_id + 1

    # 创建完整日记条目
    diary_entry = {
        "username": username,
        "id": new_id,
        "title": title,
        "content": content,
        "image": images,
        "video": videos,
        "views": 0,
        "rating": 0.0,
        "tags": tags,
        "timestamp": int(time.time())  # 保留原有时间戳功能
    }

    # 更新并写入完整列表
    diaries.append(diary_entry)
    write_json(DIARIES_FILE, diaries)

def get_diaries(username: str) -> list:
    """
    根据用户名查询日记：
    - 添加按id降序排列（最新在前）
    - 保持其他过滤逻辑不变
    """
    diaries = read_json(DIARIES_FILE, default=[])
    if(username == "__all__"):
        return sorted(diaries, key=lambda x: x["id"], reverse=True)
    else:
        user_diaries = [entry for entry in diaries if entry.get("username") == username]
        return sorted(user_diaries, key=lambda x: x["id"], reverse=True)