from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models.diaries import Diary
from app.services import diary_service

router = APIRouter(tags=["日记管理"])

@router.post("", response_model=dict, summary="添加游记")
def add_diary(diary: Diary):
    """
    添加日记接口：
      - 将日记信息保存到持久化存储（JSON 或数据库）
    """
    diary_service.add_diary(
        diary.username,
        diary.title,
        diary.content,
        diary.images,
        diary.videos,
        diary.tags
    )
    return {"message": "日记添加成功"}

@router.get("/{username}", response_model=dict, summary="获取用户游记列表")
def get_diaries(
    username: str,
    sort_key: str = Query(default="id", description="排序字段（如id/date/title/rating/views等）"),
    sort_order: str = Query(default="desc", description="排序方向：asc（升序）/desc（降序）")
):
    """
    获取用户所有日记接口：
      - 根据用户名查询并返回该用户所有日记
      - 支持自定义排序（默认按id降序）
      - 示例：/diaries/user1?sort_key=date&sort_order=asc
    """
    diaries = diary_service.get_diaries(
        username=username,
        sort_key=sort_key,
        sort_order=sort_order
    )
    return {"diaries": diaries}

@router.put("", summary="更新日记")
def update_diary(diary: Diary):
    """
    更新日记接口：
      - 接收包含 username 和 id 的 Diary 对象
      - 如果未提供 id 或找不到对应日记，返回 404
      - 仅更新传入的字段，保留其他字段不变
    """
    if diary.id is None:
        raise HTTPException(status_code=400, detail="缺少日记 ID，无法更新")
    try:
        updated = diary_service.update_diary(
            diary.username,
            diary.id,
            {
                "title": diary.title,
                "content": diary.content,
                "images": diary.images,
                "videos": diary.videos,
                "tags": diary.tags
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "日记更新成功", "diary": updated}