import math
import heapq
from app.config import MAP_FILE
from utils.file_utils import read_json


def haversine(lat1, lon1, lat2, lon2):
    """
    计算两点间的地球表面距离（米），使用 Haversine 公式
    """
    R = 6371000  # 地球半径（米）
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def a_star(start_id, end_id, mode):
    """
    在 map.json 图上执行 A* 最短路算法。

    参数:
      start_id: 起点节点 id
      end_id:   终点节点 id
      mode: 0 - 最短距离（米）
            1 - 步行最短时间（分钟）
            2 - 自行车最短时间（分钟）
            3 - 电动车最短时间（分钟）

    返回: (cost, path_nodes)
      cost: 最短路长度（米）或最短时间（分钟），保留两位小数
      path_nodes: 路径上节点的完整信息列表
    """
    # 读取图数据
    graph = read_json(MAP_FILE, default={})
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])

    # 构造节点索引和邻接表
    node_index = {node['id']: node for node in nodes}
    adjacency = {nid: [] for nid in node_index}
    for edge in edges:
        u, v = edge['start_node'], edge['end_node']
        adjacency[u].append(edge)
        adjacency[v].append(edge)

    # 计算全局最大速度，用于初始启发估价（m/s）
    max_walk = max((e['walk_speed'] for e in edges), default=1.0)
    max_bike = max((e['bike_speed'] for e in edges), default=3.0)
    max_ebike = max((e['ebike_speed'] for e in edges), default=1e-6)
    default_speeds = {1: max_walk, 2: max_bike, 3: max_ebike}

    # 启发函数：两点直线距离（米）
    def heuristic(nid):
        n = node_index[nid]
        t = node_index[end_id]
        return haversine(n['latitude'], n['longitude'], t['latitude'], t['longitude'])

    # 初始化 g, f 分数
    inf = float('inf')
    g_score = {nid: inf for nid in node_index}
    f_score = {nid: inf for nid in node_index}
    g_score[start_id] = 0

    # 初始估价
    if mode == 0:
        # 距离模式
        f_score[start_id] = heuristic(start_id)
    else:
        # 时间模式，启发式需转换为分钟
        speed = default_speeds.get(mode, 1.0)
        h0 = heuristic(start_id) / speed / 60 if speed >= 0.01 else inf
        f_score[start_id] = h0

    # open set 使用小顶堆
    open_set = []  # 元素为 (f_score, node_id)
    heapq.heappush(open_set, (f_score[start_id], start_id))
    came_from = {}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end_id:
            # 重建路径
            path = []
            nid = end_id
            while nid in came_from:
                path.append(node_index[nid])
                nid = came_from[nid]
            path.append(node_index[start_id])
            path.reverse()
            return round(g_score[end_id], 2), path

        for edge in adjacency[current]:
            neighbor = edge['end_node'] if edge['start_node'] == current else edge['start_node']
            dist = edge['distance']  # 米
            if mode == 0:
                # 距离成本
                tentative_g = g_score[current] + dist
                h = heuristic(neighbor)
            else:
                # 时间成本（分钟），速度 <0.01 m/s 则不可通行
                speed = edge['walk_speed'] if mode == 1 else (edge['bike_speed'] if mode == 2 else edge['ebike_speed'])
                if speed < 0.01:
                    continue
                # dist/speed 得秒，转换为分钟需/60
                time_cost = dist / speed / 60
                tentative_g = g_score[current] + time_cost
                h = heuristic(neighbor) / speed / 60

            tentative_f = tentative_g + h
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_f
                heapq.heappush(open_set, (tentative_f, neighbor))

    # 无路径
    return inf, []


# 示例调用
if __name__ == '__main__':
    cost, path = a_star(8, 12, 1)
    print(f"最优花费: {cost} 分钟")
    print("路径:")
    for n in path:
        print(n)
