import sys
import os

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取当前目录的父目录（即项目根目录）
project_root = os.path.dirname(current_dir)

# 将项目根目录添加到 sys.path 中
sys.path.append(project_root)

from app.services.map_service import a_star

distance, time, path = a_star("留学生公寓", "学六公寓", 0)
print(f"最短路径: {distance} 米")
print(f"最短时间: {time} 分钟")
print("路径:")
for n in path:
    print(n)