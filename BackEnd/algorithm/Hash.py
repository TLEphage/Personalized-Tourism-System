def simple_hash(s: str) -> str:
    """
    使用简单算法实现的哈希函数。
    算法说明：对字符串中的每个字符，
    使用一个素数累乘并加上字符的 ASCII 码，结果对一个大质数取模。
    
    注意：该算法仅用于演示目的，安全性极低！
    """
    hash_val = 0
    mod = 10**9 + 7  # 大质数
    for ch in s:
        # 131 为常用的乘数
        hash_val = (hash_val * 131 + ord(ch)) % mod
    return str(hash_val)