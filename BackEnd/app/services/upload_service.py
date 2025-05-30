import os
from app.config import IMAGES_DIR

def upload_image(file_contents: bytes, filename: str):
    # 保存文件
    file_path = os.path.join(IMAGES_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(file_contents)
    
    return {"filename": filename, "url": file_path}