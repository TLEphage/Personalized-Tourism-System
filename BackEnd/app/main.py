from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# 导入路由模块
from app.routers import upload, users, diaries, spots, map, foods, AIGen
from app.config import *

# --------------------------- 初始化 FastAPI 应用 ---------------------------
app = FastAPI(
    title="旅游系统后端 API",
    description="提供用户管理、日记发布、路径规划等功能接口",
    version="1.0.0",
    openapi_tags=[  # 定义 Swagger 文档的标签分组
        {
            "name": "文件上传",
            "description": "图片、视频等文件上传"
        },
        {
            "name": "用户管理",
            "description": "用户注册、登录、信息查询与修改"
        },
        {
            "name": "日记管理",
            "description": "日记的增删改查与排序"
        },
        {
            "name": "景点查询",
            "description": "景点的查询与排序"
        },
        {
            "name": "地图查询",
            "description": "旅游路线规划与场所查询"
        },
        {
            "name": "美食搜索",
            "description": "美食的查询与排序"
        },
        {
            "name": "生成式AI服务",
            "description": "文生视频和智能体的API调用"
        }
    ]
)

# --------------------------- 配置 CORS 中间件 ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 允许所有来源（生产环境请根据域名白名单配置）
    allow_credentials=True,     # 允许携带凭证（如 Cookie）
    allow_methods=["*"],        # 允许所有 HTTP 方法
    allow_headers=["*"],        # 允许所有请求头
)

# --------------------------- 集成路由模块 ---------------------------

# 挂载静态文件目录，用于访问上传的图片
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")
# 挂载静态文件目录，用于访问生成的视频
app.mount("/videos", StaticFiles(directory=VIDEO_DIR), name="videos")

# 文件上传路由（前缀 /upload，标签"文件上传"）
app.include_router(
    upload.router,
    prefix="/upload",  # 统一前缀，如 /upload/image
    tags=["文件上传"]  # 对应 openapi_tags 中的标签名
)

# 用户管理路由（前缀 /users，标签"用户管理"）
app.include_router(
    users.router,
    prefix="/users",
    tags=["用户管理"]
)

# 日记管理路由（前缀 /diaries，标签"日记管理"）
app.include_router(
    diaries.router,
    prefix="/diaries",
    tags=["日记管理"]
)

# 景点查询路由（前缀 /spots，标签"景点查询"）
app.include_router(
    spots.router,
    prefix="/spots",
    tags=["景点查询"]
)

# 地图查询路由（前缀 /map，标签"地图查询"）
app.include_router(
    map.router,
    prefix="/map",
    tags=["地图查询"]
)

# 美食搜索路由（前缀 /foods，标签"美食搜索"）
app.include_router(
    foods.router,
    prefix="/foods",
    tags=["美食搜索"]
)

# 生成式AI服务路由（前缀 /AIGen，标签"生成式AI服务"）
app.include_router(
    AIGen.router,
    prefix="/AIGen",
    tags=["生成式AI服务"]
)

# --------------------------- 根路径测试端点 ---------------------------
@app.get("/", summary="服务状态检查")
def home():
    """
    根路径测试接口，用于检查服务是否正常运行。
    
    - 返回简单的 JSON 响应
    """
    return {"message": "旅游系统后端服务运行正常，请访问 /docs 查看完整 API 文档"}

# --------------------------- 本地调试启动 ---------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",  # 模块路径:FastAPI 实例名
        host="0.0.0.0",  # 允许所有 IP 访问
        port=8000,       # 端口号
        reload=True      # 开发时启用热重载
    )