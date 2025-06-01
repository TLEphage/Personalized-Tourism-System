from pydantic import BaseModel
from typing import Optional, List

class DiaryRequest(BaseModel):
    """日记请求模型"""
    username: str
    id: Optional[int] = None  # 更新日记时需要
    title: str
    content: str
    images: Optional[List[str]] = None
    videos: Optional[List[str]] = None
    tags: Optional[List[str]] = None

class DiaryTagRequest(BaseModel):
    """日记打标签请求模型"""
    id: int
    tag: str

class DiaryResponse(BaseModel):
    """日记响应模型"""
    username: str
    id: int
    title: str
    content: str
    images: List[str]
    videos: List[str]
    tags: List[str]
    views: int
    rating: float
    tags: List[str]
    timestamp: int
