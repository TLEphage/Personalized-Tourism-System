from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Optional, List
from app.services import user_service, diary_service, map_service

# 定义请求和响应数据模型
class UserCreate(BaseModel):
    """用户注册请求模型"""
    username: str
    password: str

class UserLogin(BaseModel):
    """用户登录请求模型"""
    username: str
    password: str

class UserResponse(BaseModel):
    """用户信息响应模型"""
    id: int
    username: str
    role: str
    avatarPath: Optional[str] = None
    signature: Optional[str] = None
    hobbies: Optional[List[str]] = None

class MapRequest(BaseModel):
    start: str  # 起点标识，可以根据实际需要调整数据类型
    end: str    # 终点标识

class Diary(BaseModel):
    username: str
    title: str
    content: str
    images: list = None
    videos: list = None
    tags: list = None

app = FastAPI(title="旅游系统后端 API")

# 添加 CORS 中间件（必须放在其他路由和中间件之前）
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（生产环境应限制为具体域名）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法（包括 OPTIONS）
    allow_headers=["*"],  # 允许所有请求头
)

@app.get("/")
def home():
    return {"message": "旅游系统后端服务已运行，请访问 /docs 查看接口文档"}

# 用户注册接口
@app.post("/register")
def register(user: UserCreate):
    if user_service.register(user.username, user.password):
        return {"message": "注册成功"}
    else:
        raise HTTPException(status_code=400, detail="注册失败，用户名已存在")

# 用户登录接口
@app.post("/login")
def login(user: UserLogin):
    login_information = user_service.login(user.username, user.password)
    if login_information.get("id", False):
        return login_information["user"]
    elif login_information.get("message","") == "密码错误":
        raise HTTPException(status_code=400, detail="密码错误")
    else:
        raise HTTPException(status_code=400, detail="用户名不存在")

@app.get("/users/{username}")
def get_user(username: str):
    user = user_service.get_user([], username)
    if user:
        return UserResponse(**user)
    raise HTTPException(status_code=404, detail="用户不存在")

# 最短路径规划接口，使用A*算法
@app.post("/shortest_path")
def shortest_path(map_req: MapRequest):
    path = map_service.a_star(map_req.start, map_req.end)
    if path:
        return {"shortest_path": path}
    else:
        raise HTTPException(status_code=404, detail="未能找到合适的路径")

# 日记存储接口
@app.post("/diaries")
def add_diary(diary: Diary):
    diary_service.add_diary(
        diary.username, 
        diary.title, 
        diary.content, 
        diary.images, 
        diary.videos, 
        diary.tags
    )
    return {"message": "日记添加成功"}

# 日记读取接口，根据用户名查询该用户所有日记
@app.get("/diaries/{username}")
def get_diaries(username: str):
    diaries = diary_service.get_diaries(username)
    return {"diaries": diaries}

# 启动服务
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
