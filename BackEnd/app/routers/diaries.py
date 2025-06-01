from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models.diaries import DiaryRequest, DiaryTagRequest, DiaryResponse
from app.services import diary_service

router = APIRouter(tags=["日记管理"])

@router.post("/add", response_model=dict, summary="添加日记")
def add_diary(diary: DiaryRequest):
    """
    添加日记接口：
      - 将日记信息保存到持久化存储（JSON 或数据库）
    """
    print(diary)
    diary_service.add_diary(
        diary.username,
        diary.title,
        diary.content,
        diary.images,
        diary.videos,
        diary.tags
    )
    return {"message": "日记添加成功"}

@router.post("/details/{diary_id}", response_model=DiaryResponse, summary="获取特定id的日记")
def get_diary(diary_id: int):
    try:
        response = diary_service.get_diary(diary_id)
        if response.get("message") == "查找成功":
            return response.get("diary")
    except ValueError as e:
        raise HTTPException(status_code=404, detail="日记未找到")

@router.get("/{username}", response_model=dict, summary="获取用户游记列表")
def get_user_diaries(
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
    diaries = diary_service.get_user_diaries(
        username=username,
        sort_key=sort_key,
        sort_order=sort_order
    )
    return {"diaries": diaries}

@router.post("/update", response_model=dict, summary="更新日记")
def update_diary(diary: DiaryRequest):
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

@router.post("/tag", response_model=dict, summary="给对应id的日记打标签")
def get_diary(diary: DiaryTagRequest):
    try:
        response = diary_service.diary_append(diary.id, "tags", diary.tag)
        return {"message": "标签添加成功", "diary": response["diary"]}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))