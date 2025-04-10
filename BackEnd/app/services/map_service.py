import heapq
from app.config import MAP_FILE
from utils.file_utils import read_json

def heuristic(a: str, b: str) -> int:
    """
    简单启发式函数（此处返回 0，使 A* 算法退化为 Dijkstra 算法）。
    """
    return 0

def a_star(start: str, goal: str):
    """
    使用 A* 算法寻找从 start 到 goal 的最短路径
      - 从 MAP_FILE 中读取图数据（字典结构）
      - 如果起点或终点不存在，则返回 None
      - 返回找到的路径列表，如：["A", "B", "C"]；若未找到则返回 None
    """
    graph = read_json(MAP_FILE, default={})
    if start not in graph or goal not in graph:
        return None

    # 使用堆实现 open_set，堆中的元素为 (f_score, node)
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}  # 用于回溯最短路径
    g_score = {node: float("inf") for node in graph}
    g_score[start] = 0
    f_score = {node: float("inf") for node in graph}
    f_score[start] = heuristic(start, goal)

    while open_set:
        current_f, current = heapq.heappop(open_set)
        if current == goal:
            # 回溯构建最短路径
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return list(reversed(path))

        for neighbor, weight in graph.get(current, {}).items():
            tentative_g_score = g_score[current] + weight
            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None
