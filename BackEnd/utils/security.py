import time
from app.algorithm.Hash import simple_hash

def hash_password(password: str) -> str:
    """
    对密码进行简单加盐哈希处理，不调用 hashlib 等库函数。
    salt 使用当前时间戳（毫秒）作为简单实现。
    
    返回格式："hashed_password:salt"
    """
    salt = str(int(time.time() * 1000))  # 以毫秒为单位的时间戳作为盐
    hashed = simple_hash(password + salt)
    return f"{hashed}:{salt}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """
    验证用户提供的密码是否与存储的哈希值匹配。
    解析出存储的 salt，并重新计算哈希做比对。
    """
    try:
        hashed_password, salt = stored_password.split(":")
    except ValueError:
        # 格式不正确，验证失败
        return False
    provided_hash = simple_hash(provided_password + salt)
    return provided_hash == hashed_password

def create_token(data: dict, expires_in: int = 3600) -> str:
    """
    使用简单算法生成 token，不调用 jwt 库。
    token 格式为： data_str|expiry|hash，其中：
      - data_str：将 data 中的键值对用逗号拼接，如 "user:alice,role:admin"
      - expiry：token 的过期时间戳（当前时间 + expires_in 秒）
      - hash：对 data_str 和 expiry 拼接后的字符串做 simple_hash 得到的签名
    
    该 token 简单地保证了数据完整性，不建议在高安全性场景下使用！
    """
    expiry = int(time.time()) + expires_in
    # 拼接字典为字符串（注意：该实现仅支持简单情况，复杂数据请自行设计解析格式）
    data_str = ",".join(f"{k}:{v}" for k, v in data.items())
    token_raw = f"{data_str}|{expiry}"
    token_hash = simple_hash(token_raw)
    token = f"{token_raw}|{token_hash}"
    return token

def decode_token(token: str) -> dict:
    """
    解析并验证 token，如校验失败或 token 过期则返回 None。
    
    解析规则：将 token 按 "|" 分割为三部分，
      第一部分为 data_str，第二部分为 expiry，第三部分为签名。
    验证：重新计算前两部分的哈希，检查与第三部分是否一致，
      同时确认 expiry 尚未超过当前时间。
    若验证通过，则将 data_str 解析为字典后返回。
    """
    parts = token.split("|")
    if len(parts) != 3:
        return None
    data_str, expiry_str, token_hash = parts
    token_raw = f"{data_str}|{expiry_str}"
    expected_hash = simple_hash(token_raw)
    if token_hash != expected_hash:
        return None  # 签名不匹配
    if int(expiry_str) < int(time.time()):
        return None  # Token 已过期

    # 解析 data_str 还原为字典
    data = {}
    if data_str:
        items = data_str.split(",")
        for item in items:
            if ":" in item:
                k, v = item.split(":", 1)
                data[k] = v
    return data

# 调试测试（仅演示用，可删除）
if __name__ == "__main__":
    # 密码哈希与验证
    original_password = "my_secret"
    stored = hash_password(original_password)
    print("存储的密码:", stored)
    assert verify_password(stored, original_password)
    assert not verify_password(stored, "wrong_password")
    
    # Token 创建与解析
    token = create_token({"user": "alice", "role": "admin"}, expires_in=60)
    print("生成的 token:", token)
    decoded = decode_token(token)
    print("解析 token 后的数据:", decoded)
