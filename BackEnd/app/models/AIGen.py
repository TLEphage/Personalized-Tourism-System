from pydantic import BaseModel

class TextToVideoRequest(BaseModel):
    username: str
    diary_id: int
    prompt: str
    quality: str = "speed"

class ImageToVideoRequest(BaseModel):
    username: str
    diary_id: int
    prompt: str = "让画面动起来"
    image_url: str
    quality: str = "speed"