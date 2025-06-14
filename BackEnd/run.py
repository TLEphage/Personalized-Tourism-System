from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uvicorn
from typing import Optional, List, Dict
from app.services import user_service, diary_service, map_service

# 定义 FastAPI 实例，标题为“旅游系统后端 API”
app = FastAPI(title="旅游系统后端 API")

# 添加 CORS 中间件，放在路由前，允许跨域请求
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 允许所有来源（生产环境请根据域名白名单配置）
    allow_credentials=True,      # 允许携带凭证（如 Cookie）
    allow_methods=["*"],       # 允许所有 HTTP 方法
    allow_headers=["*"],       # 允许所有请求头
)

@app.get("/")
def home():
    """
    根路径，返回服务运行状态提示。
    """
    return {"message": "旅游系统后端服务已运行，请访问 /docs 查看接口文档"}

# --------------------------- 用户相关接口 ---------------------------

class UserCreate(BaseModel):
    """
    用户注册请求模型：
      - username: 用户名
      - password: 密码
    """
    username: str
    password: str

class UserLogin(BaseModel):
    """
    用户登录请求模型：
      - username: 用户名
      - password: 密码
    """
    username: str
    password: str

class UserUpdate(BaseModel):
    """
    用户信息更新请求模型，可选字段：
      - avatarPath: 头像路径
      - signature: 个性签名
      - hobbies: 兴趣爱好列表
    """
    avatarPath: Optional[str] = None
    signature: Optional[str] = None
    hobbies: Optional[List[str]] = None

class UserResponse(BaseModel):
    """
    用户信息响应模型，返回给前端：
      - id: 用户唯一标识
      - username: 用户名
      - role: 用户角色
      - avatarPath: 头像存储路径
      - signature: 个性签名
      - hobbies: 爱好列表
    """
    id: int
    username: str
    role: str
    avatarPath: Optional[str] = None
    signature: Optional[str] = None
    hobbies: Optional[List[str]] = None

@app.post("/users/register")
def register(user: UserCreate):
    """
    用户注册接口：
      - 接收用户名和密码
      - 如果用户名已存在，返回 400 错误；否则注册新用户
    """
    if user_service.register(user.username, user.password):
        return {"message": "注册成功"}
    else:
        raise HTTPException(status_code=400, detail="用户名已存在")

@app.post("/users/login")
def login(user: UserLogin):
    """
    用户登录接口：
      - 验证用户名和密码
      - 成功返回用户信息；失败抛出 400 错误
    """
    login_info = user_service.login(user.username, user.password)
    if login_info.get("success", False):
        return login_info["user"]
    else:
        raise HTTPException(status_code=400, detail=login_info.get("message", ""))

@app.get("/users/{username}/details")
def get_user(username: str):
    """
    查询用户信息接口：
      - 根据用户名获取用户基本信息
      - 找不到时返回 404 错误
    """
    user = user_service.get_user([], username)
    if user:
        return UserResponse(**user)
    raise HTTPException(status_code=404, detail="用户不存在")

@app.put("/users/{username}")
def update_user(username: str, update: UserUpdate):
    """
    修改用户信息接口：
      - 可更新 avatarPath、signature、hobbies
      - 返回更新后的用户信息；找不到用户返回 404 错误
    """
    try:
        # 使用 Pydantic v2 推荐的 model_dump 方法，exclude_unset=True 仅传递实际更新字段
        updated_user = user_service.update_user(username, update.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "用户信息更新成功", "user": updated_user}

# --------------------------- 景点查询接口 ---------------------------




# --------------------------- 路径规划接口 ---------------------------

class PathPlanRequest(BaseModel):
    """
    路径规划请求模型：
      - start: 起点名称
      - end: 终点名称
      - mode: 规划模式（0: 最短路径，1: 步行最短时间，2: 自行车最短时间，3: 电动车最短时间）
    """
    start: str
    end: str
    mode: int

class PathPlanResponse(BaseModel):
    """
    路径规划响应模型：
      - distance: 距离（米）
      - time: 时间（秒）
      - path: 路径节点列表
    """
    distance: float
    time: float
    path: list

@app.post("/map/path_plan")
def path_plan(map_req: PathPlanRequest):
    """
    A* 算法路径规划：
      - 根据请求参数调用 map_service.a_star 方法
      - 如果找不到路径，抛出 404 错误
    """
    distance, time, path = map_service.a_star(map_req.start, map_req.end, map_req.mode)
    if distance == float('inf'):
        raise HTTPException(status_code=404, detail="未能找到合适的路径")
    return PathPlanResponse(distance=distance, time=time, path=path)

# --------------------------- 日记管理接口 ---------------------------

class Diary(BaseModel):
    """
    日记请求模型：
      - username: 用户名
      - title: 日记标题
      - content: 日记内容
      - images: 可选图片列表
      - videos: 可选视频列表
      - tags: 可选标签列表
    """
    username: str
    id: Optional[int] = None  # 可选，更新日记时需要
    title: str
    content: str
    images: Optional[List[str]] = None
    videos: Optional[List[str]] = None
    tags: Optional[List[str]] = None

@app.post("/diaries")
def add_diary(diary: Diary):
    """
    添加日记接口：
      - 将日记信息保存到持久化存储（JSON 或数据库）
    """
    diary_service.add_diary(
        diary.username,
        diary.title,
        diary.content,
        diary.images,
        diary.videos,
        diary.tags
    )
    return {"message": "日记添加成功"}

@app.get("/diaries/{username}")
def get_diaries(
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
    diaries = diary_service.get_diaries(
        username=username,
        sort_key=sort_key,
        sort_order=sort_order
    )
    return {"diaries": diaries}

@app.put("/diaries")
def update_diary(diary: Diary):
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

# 启动服务，指定主机和端口
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)