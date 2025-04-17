import os
from app.config import USERS_FILE, USERS_AVATARS_DIR
from utils.file_utils import read_json, write_json
from utils.security import hash_password, verify_password, create_token

def get_max_id(users):
    if not users:
        return 0
    return max(user['id'] for user in users)

def register(username: str, password: str) -> bool:
    """
    注册新用户：
      - 先从 JSON 文件中读取所有用户数据
      - 如果用户名已存在，则返回 False
      - 否则，对密码进行哈希处理，并保存到文件中，返回 True
    """
    users = read_json(USERS_FILE, default={})
    if any(user.get("username","") == username for user in users):
        return False
    passwordHash = hash_password(password)
    new_user = {
        'id': get_max_id(users)+1,
        'username': username,
        'passwordHash': passwordHash,
        'role': "admin",
        'avatarPath': os.path.join(USERS_AVATARS_DIR, "default_avatar.jpg"),
        'signature': None,
        'hobbies': None
    }
    users.append(new_user)
    write_json(USERS_FILE, users)
    return True

def get_user(users: list, username: str) -> dict:
    """获取用户信息"""
    if not users:
        users = read_json(USERS_FILE, default={})
    for user in users:
        if user.get("username") == username:
            return {
                "id": user.get("id", -1),
                "username": user.get("username", ""),
                "passwordHash": user.get("passwordHash", ""),
                "role": user.get("role", ""),
                "avatarPath": user.get("avatarPath", os.path.join(USERS_AVATARS_DIR, "default_avatar.jpg")),
                "signature": user.get("signature", ""),
                "hobbies": user.get("hobbies", [])
            }
    return None

def login(username: str, password: str) -> dict:
    """
    用户登录：
      - 从文件中读取用户数据，
      - 若用户名不存在或密码验证失败则返回失败信息，
      - 否则，返回成功信息和用户信息。
    """
    users = read_json(USERS_FILE, default={})
    user = get_user(users, username)
    if user is None:
        return {
            "success": False,
            "message": "用户名不存在"
        }
    stored_password = user.get("passwordHash","")
    if not verify_password(stored_password, password):
        return {
            "success": False,
            "message": "密码错误"
        }
    return {
        "success": True,
        "message": "登录成功",
        "user": {
            "id": user.get("id", -1),
            "username": user.get("username", ""),
            "role": user.get("role", ""),
            "avatarPath": user.get("avatarPath",  os.path.join(USERS_AVATARS_DIR, "default_avatar.jpg")),
            "signature": user.get("signature", ""),
            "hobbies": user.get("hobbies", [])
        }
    }