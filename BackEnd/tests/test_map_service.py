import sys
import os

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取当前目录的父目录（即项目根目录）
project_root = os.path.dirname(current_dir)

# 将项目根目录添加到 sys.path 中
sys.path.append(project_root)

from app.services.map_service import a_star

cost, path = a_star(8, 12, 2)
print(f"最优花费: {cost}")
print("路径:")
for n in path:
    print(n)