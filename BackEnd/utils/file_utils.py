import json
import os
from app.algorithm.HuffmanCompressor import HuffmanCompressor

def read_json(file_path, default=None):
    """
    读取 JSON 文件并返回数据。
    如果文件不存在，则返回 default（默认为 None）。
    """
    if not os.path.exists(file_path):
        return default if default is not None else {}
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = default if default is not None else {}
    return data

def write_json(file_path, data):
    """
    将数据写入指定 JSON 文件，保存时格式化为可读的形式。
    """
    # 创建父目录（如果不存在）
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def append_json(file_path, new_data):
    """
    如果 JSON 文件中数据是列表，则附加数据到列表尾部；
    如果文件不存在，则创建一个新列表，并写入 new_data。
    """
    data = read_json(file_path, default=[])
    if isinstance(data, list):
        data.append(new_data)
    else:
        # 如果已有数据不是列表，则将其转换为列表形式存储
        data = [data, new_data]
    write_json(file_path, data)

def read_compressed_json(filepath: str, default=None):
    try:
        with open(filepath, 'rb') as f:
            compressed = f.read()
        if not compressed:
            return default if default is not None else []
        decompressed = HuffmanCompressor.decompress(compressed)
        return json.loads(decompressed)
    except Exception as e:
        raise IOError(f"读取失败: {str(e)}")

def write_compressed_json(filepath: str, data):
    try:
        json_str = json.dumps(data, ensure_ascii=False)
        compressed = HuffmanCompressor.compress(json_str)
        with open(filepath, 'wb') as f:
            f.write(compressed)
    except Exception as e:
        raise IOError(f"写入失败: {str(e)}")