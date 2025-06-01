from fastapi import APIRouter, HTTPException, Query
from app.models.AIGen import VideoRequest
from app.services.AIGen_service import generate_video_request, check_all_video_status

router = APIRouter(tags=["生成式AI服务"])

@router.post("/generate_video", summary="文生视频")
async def generate_video(request: VideoRequest):
    """生成视频并添加到生成队列"""
    print(request)
    response = generate_video_request(
        request.username,
        request.diary_id,
        request.prompt,
        request.quality
    )
    return response

@router.post("/check_video_status", summary="检查视频生成状态")
async def get_video_status():
    """获取视频生成状态"""
    response = check_all_video_status()
    return response