import os

# 当前文件所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据文件目录（data 文件夹位于 app 目录下）
DATA_DIR = os.path.join(BASE_DIR, "data")

# 用户数据文件路径
USERS_FILE = os.path.join(DATA_DIR, "users.json")
# 用户头像文件目录
USERS_AVATARS_DIR = os.path.join(DATA_DIR, "avatars")
# 图片文件目录
IMAGES_DIR = os.path.join(DATA_DIR, "images")
# 日记数据文件路径
DIARIES_FILE = os.path.join(DATA_DIR, "diaries.json")
# 地图数据文件路径（存储图结构数据，格式示例：{"A": {"B": 1, "C": 4}, "B": {"A": 1, "C": 2, "D": 5}, ...}）
MAP_FILE = os.path.join(DATA_DIR, "map.json")
# 中国景点文件路径
SPOTS_FILE = os.path.join(DATA_DIR, "spots.json")
# 美食文件路径
FOODS_FILE = os.path.join(DATA_DIR, "foods.json")