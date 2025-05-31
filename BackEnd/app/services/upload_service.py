import os
from app.config import IMAGES_DIR

def upload_image(path: str, file_contents: bytes, filename: str):
    # 保存文件
    path = path.lstrip("/")
    folder_path = os.path.join(IMAGES_DIR, path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "wb") as f:
        f.write(file_contents)
    
    return {"filename": filename, "url": file_path}