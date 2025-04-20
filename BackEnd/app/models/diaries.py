from pydantic import BaseModel
from typing import Optional, List

class Diary(BaseModel):
    """
    日记请求模型：
      - username: 用户名
      - title: 日记标题
      - content: 日记内容
      - images: 可选图片列表
      - videos: 可选视频列表
      - tags: 可选标签列表
    """
    username: str
    id: Optional[int] = None  # 可选，更新日记时需要
    title: str
    content: str
    images: Optional[List[str]] = None
    videos: Optional[List[str]] = None
    tags: Optional[List[str]] = None