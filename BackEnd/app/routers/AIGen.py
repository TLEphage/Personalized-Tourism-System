from fastapi import APIRouter, HTTPException, Query
from app.models.AIGen import TextToVideoRequest, ImageToVideoRequest
from app.services.AIGen_service import generate_video_request, check_all_video_status

router = APIRouter(tags=["生成式AI服务"])

@router.post("/text_generate_video", summary="文生视频")
async def text_generate_video(request: TextToVideoRequest):
    """生成视频并添加到生成队列"""
    print(request)
    response = generate_video_request(
        username=request.username,
        diary_id=request.diary_id,
        image_url="",
        prompt=request.prompt,
        quality=request.quality
    )
    return response

@router.post("/image_generate_video", summary="图生视频")
async def image_generate_video(request: ImageToVideoRequest):
    """生成视频并添加到生成队列"""
    print(request)
    response = generate_video_request(
        username=request.username,
        diary_id=request.diary_id,
        image_url=request.image_url,
        prompt=request.prompt,
        quality=request.quality
    )
    return response

@router.post("/check_video_status", summary="检查视频生成状态")
async def get_video_status():
    """获取视频生成状态"""
    response = check_all_video_status()
    return response