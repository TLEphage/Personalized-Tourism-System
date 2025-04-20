from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入路由模块
from app.routers import users, diaries, spots, map

# --------------------------- 初始化 FastAPI 应用 ---------------------------
app = FastAPI(
    title="旅游系统后端 API",
    description="提供用户管理、游记发布、路径规划等功能接口",
    version="1.0.0",
    openapi_tags=[  # 定义 Swagger 文档的标签分组
        {
            "name": "用户管理",
            "description": "用户注册、登录、信息查询与修改"
        },
        {
            "name": "游记管理",
            "description": "游记的增删改查与排序"
        },
        {
            "name": "景点查询",
            "description": "景点的查询与排序"
        },
        {
            "name": "路径规划",
            "description": "基于 A* 算法的路径规划功能"
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
# 用户管理路由（前缀 /users，标签"用户管理"）
app.include_router(
    users.router,
    prefix="/users",  # 统一前缀，如 /users/register
    tags=["用户管理"]  # 对应 openapi_tags 中的标签名
)

# 游记管理路由（前缀 /diaries，标签"游记管理"）
app.include_router(
    diaries.router,
    prefix="/diaries",
    tags=["游记管理"]
)

app.include_router(
    spots.router,
    prefix="/spots",
    tags=["景点查询"]
)

# 路径规划路由（前缀 /map，标签"路径规划"）
app.include_router(
    map.router,
    prefix="/map",
    tags=["路径规划"]
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