from pydantic import BaseModel

class VideoRequest(BaseModel):
    username: str
    diary_id: int
    prompt: str
    quality: str = "speed"