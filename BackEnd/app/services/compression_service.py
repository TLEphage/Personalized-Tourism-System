import json
import zlib
from typing import List

def compress_diaries(data: List[dict], output_file: str = "data/diaries.json.zlib") -> None:
    """
    将日记数据压缩并保存为 zlib 格式
    """
    json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    compressed = zlib.compress(json_data)
    with open(output_file, 'wb') as f:
        f.write(compressed)

def decompress_diaries(input_file: str = "data/diaries.json.zlib") -> List[dict]:
    """
    解压 zlib 格式文件并还原为原始日记数据
    """
    with open(input_file, 'rb') as f:
        compressed = f.read()
    json_data = zlib.decompress(compressed).decode('utf-8')
    return json.loads(json_data)