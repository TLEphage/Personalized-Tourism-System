from fastapi import APIRouter, HTTPException
from app.models.users import UserCreate, UserLogin, UserUpdate, UserResponse
from app.services import user_service

router = APIRouter(tags=["用户管理"])

@router.post("/register", response_model=dict, summary="用户注册")
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

@router.post("/login", response_model=UserResponse, summary="用户登录")
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

@router.get("/{username}/details", response_model=UserResponse, summary="查询用户信息")
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

@router.put("/{username}/details", summary="修改用户信息")
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