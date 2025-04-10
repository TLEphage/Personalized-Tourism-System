import time
from app.config import DIARIES_FILE
from utils.file_utils import read_json, write_json, append_json

def add_diary(username: str, content: str):
    """
    添加日记：
      - 根据传入的用户名和内容生成一个日记条目（附加时间戳）
      - 追加写入到 diaries.json 中（假设文件中存储的是一个列表）
    """
    diary_entry = {
        "username": username,
        "content": content,
        "timestamp": int(time.time())
    }
    append_json(DIARIES_FILE, diary_entry)

def get_diaries(username: str) -> list:
    """
    根据用户名查询日记：
      - 从文件中读取所有日记条目，
      - 过滤出对应用户名的日记并返回
    """
    diaries = read_json(DIARIES_FILE, default=[])
    return [entry for entry in diaries if entry.get("username") == username]
