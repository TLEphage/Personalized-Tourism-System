import os
from app.config import USERS_FILE, USERS_AVATARS_DIR, LOCAL_STORAGE
from utils.file_utils import read_json, write_json
from utils.security import hash_password, verify_password
from app.models.users import UserResponse

def get_max_id(users):
    """
    获取当前用户列表中的最大 ID，用于新用户注册时生成自增 ID。
    """
    if not users:
        return 0
    return max(user['id'] for user in users)


def register(username: str, password: str) -> bool:
    """
    注册新用户：
      1. 从 JSON 文件读取所有用户
      2. 校验用户名是否已存在
      3. 对密码进行哈希处理
      4. 生成用户对象并追加到列表
      5. 写回 JSON 文件
    返回 True 表示注册成功，False 表示用户名已存在
    """
    users = read_json(USERS_FILE, default=[])
    if any(user.get("username", "") == username for user in users):
        return False
    passwordHash = hash_password(password)
    new_user = {
        'id': get_max_id(users) + 1,
        'username': username,
        'passwordHash': passwordHash,
        'role': "admin",  # 默认角色，可后续扩展
        'avatarPath': "http://localhost:8000/images/avatars/default_avatar.jpg",
        'signature': None,
        'hobbies': []
    }
    users.append(new_user)
    write_json(USERS_FILE, users)
    return True


def get_user(users: list, username: str) -> dict:
    """
    获取指定用户名的用户基本信息：
      - 从传入列表或文件加载用户列表
      - 找到匹配用户名，返回去除密码 Hash 的用户字典
      - 如果不存在，返回 None
    """
    if not users:
        users = read_json(USERS_FILE, default=[])
    for user in users:
        if user.get("username") == username:
            return {
                'id': user.get('id', -1),
                'username': user.get('username', ''),
                'role': user.get('role', ''),
                'avatarPath': user.get('avatarPath', "http://localhost:8000/images/avatars/default_avatar.jpg"),
                'signature': user.get('signature'),
                'hobbies': user.get('hobbies', [])
            }
    return None


def login(username: str, password: str) -> dict:
    """
    用户登录：
      1. 从文件加载所有用户
      2. 根据用户名查找用户对象
      3. 验证输入密码与存储 Hash 是否匹配
      4. 返回登录结果字典，包含 success、message、user
    """
    users = read_json(USERS_FILE, default=[])
    # 调用 get_user 获取不含密码 Hash 的用户字典
    user = get_user(users, username)
    if user is None:
        return {"success": False, "message": "用户名不存在"}
    # 从原始文件再读取密码 Hash
    raw_users = read_json(USERS_FILE, default=[])
    stored_hash = next(u['passwordHash'] for u in raw_users if u['username'] == username)
    if not verify_password(stored_hash, password):
        return {"success": False, "message": "密码错误"}
    return {"success": True, "message": "登录成功", "user": user}


def update_user(username: str, fields: dict) -> dict:
    """
    更新指定用户名的用户信息。
    支持更新的字段包括 avatarPath、signature、hobbies。
    成功后写回文件并返回最新的用户信息字典；
    用户不存在时抛出 ValueError。
    """
    users = read_json(USERS_FILE, default=[])
    for user in users:
        if user.get('username') == username:
            # 按需更新字段
            for key, value in fields.items():
                if key in ('username', 'avatarPath', 'signature', 'hobbies'):
                    user[key] = value
            write_json(USERS_FILE, users)
            # 返回清洗后的用户信息
            return {
                'id': user.get('id', -1),
                'username': user.get('username', ''),
                'role': user.get('role', ''),
                'avatarPath': user.get('avatarPath'),
                'signature': user.get('signature'),
                'hobbies': user.get('hobbies')
            }
    # 未找到用户，抛出异常，上层接口捕获并返回 404
    raise ValueError("用户不存在")

def write_local_storage(user_state: UserResponse):
    write_json(LOCAL_STORAGE,user_state)

def read_local_storage() -> UserResponse:
    return read_json(LOCAL_STORAGE)

write_local_storage({"username": None})