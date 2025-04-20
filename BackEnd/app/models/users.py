from pydantic import BaseModel
from typing import Optional, List

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