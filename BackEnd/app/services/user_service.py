from app.config import USERS_FILE
from utils.file_utils import read_json, write_json
from utils.security import hash_password, verify_password, create_token

def register(username: str, password: str) -> bool:
    """
    注册新用户：
      - 先从 JSON 文件中读取所有用户数据（以字典形式存储：{username: hashed_password}）
      - 如果用户名已存在，则返回 False
      - 否则，对密码进行哈希处理，并保存到文件中，返回 True
    """
    users = read_json(USERS_FILE, default={})
    if username in users:
        return False
    hashed = hash_password(password)
    users[username] = hashed
    write_json(USERS_FILE, users)
    return True

def login(username: str, password: str) -> str:
    """
    用户登录：
      - 从文件中读取用户数据，
      - 若用户名不存在或密码验证失败则返回 None，
      - 否则，生成一个 token 并返回。
    """
    users = read_json(USERS_FILE, default={})
    if username not in users:
        return None
    stored_password = users[username]
    if not verify_password(stored_password, password):
        return None
    # 生成 token，payload 中包含用户名
    token = create_token({"username": username})
    return token
