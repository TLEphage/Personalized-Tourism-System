from fastapi import APIRouter
from BackEnd.app.services.compression_service import decompress_diaries

router = APIRouter()

@router.get("/diaries", summary="获取所有日记", tags=["Diaries"])
def get_diaries():
    """
    解压并返回所有日记数据（来自 diaries.json.zlib 文件）
    """
    return decompress_diaries()