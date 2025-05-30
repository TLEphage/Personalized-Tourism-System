from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services import upload_service

router = APIRouter(tags=["文件上传"])

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    # print(file)
    # 验证文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="只能上传图片文件")
    contents = await file.read()
    result = upload_service.upload_image(contents, file.filename)
    return result