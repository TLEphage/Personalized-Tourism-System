import math
import heapq
from app.config import MAP_FILE
from utils.file_utils import read_json, write_json
from app.models.map import NodeRequest, EdgeRequest

def get_graph():
    graph = read_json(MAP_FILE, default={})
    return graph

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


def a_star(start_name, end_name, mode):
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
    start_id, end_id = -1, -1
    for node in nodes:
        if node.get("name", "") == start_name:
            start_id = node.get("id",-1)
        if node.get("name", "") == end_name:
            end_id = node.get("id",-1)
    if start_id == -1 or end_id == -1:
        return float('inf'), float('inf'), []

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
    distance = {nid: inf for nid in node_index} # 用于mode!=0时存放距离
    g_score[start_id] = 0
    distance[start_id] = 0
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
            return round(distance[end_id], 2), round(g_score[end_id], 2), path

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
                distance[neighbor] = distance[current] + dist
                heapq.heappush(open_set, (tentative_f, neighbor))

    # 无路径
    return float('inf'), float('inf'), []


def add_node(node_data: NodeRequest) -> dict:
    """将请求的节点加入地图数据中"""
    graph = read_json(MAP_FILE, default={})
    nodes = graph.get('nodes', [])

    if node_data.id is None:
        max_id = max((node["id"] for node in nodes), default=-1)
        node_data.id = max_id + 1

    for node in nodes:
        if node["id"] == node_data.id:
            return {"success": False, "graph": graph}
    
    new_node = {
        'id' : node_data.id,
        'name' : node_data.name,
        'type' : node_data.type,
        'popularity' : node_data.popularity,
        'longitude' : node_data.longitude,
        'latitude' : node_data.latitude,
        'connected_edges' : node_data.connected_edges
    }
    graph['nodes'].append(new_node)
    write_json(MAP_FILE, graph)
    return {"success": True, "graph": graph}

def add_edge(edge_data: EdgeRequest) -> dict:
    """将请求的边加入地图数据中"""
    graph = read_json(MAP_FILE, default={})
    if edge_data.start_node == edge_data.end_node:
        return {"success": False, "graph": graph} # 防止自环
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])

    start_node = None
    end_node = None
    for node in nodes:
        if node.get('id',-1) == edge_data.start_node:
            start_node = node
        if node.get('id',-1) == edge_data.end_node:
            end_node = node
    if start_node is None or end_node is None:
        return {"success": False, "graph": graph} # 节点不存在

    if edge_data.id is None:
        max_id = max((edge["id"] for edge in edges), default=-1)
        edge_data.id = max_id + 1

    for edge in edges:
        if edge['id'] == edge_data.id or \
        edge['start_node'] == edge_data.start_node and edge['end_node'] == edge_data.end_node or \
        edge['start_node'] == edge_data.end_node and edge['end_node'] == edge_data.start_node:
            return {"success": False, "graph": graph} # 边重复
    
    lon1 = start_node.get('longitude')
    lat1 = start_node.get('latitude')
    lon2 = end_node.get('longitude')
    lat2 = end_node.get('latitude')
    
    new_edge = {
        'id' : edge_data.id,
        'start_node' : edge_data.start_node,
        'end_node' : edge_data.end_node,
        'distance' : haversine(lat1, lon1, lat2, lon2),
        'walk_speed' : edge_data.walk_speed,
        'bike_speed' : edge_data.bike_speed,
        'ebike_speed' : edge_data.bike_speed
    }
    graph['edges'].append(new_edge)
    for node in graph['nodes']:
        if node.get('id',-1) == edge_data.start_node:
            print("start: ",node)
            node['connected_edges'].append(edge_data.id)
        if node.get('id',-1) == edge_data.end_node:
            print("end: ",node)
            node['connected_edges'].append(edge_data.id)
    write_json(MAP_FILE, graph)
    return {"success": True, "graph": graph}

# 示例调用
if __name__ == '__main__':
    distance, time, path = a_star(8, 12, 1)
    print(f"距离：{distance}, 花费: {time} 分钟")
    print("路径:")
    for n in path:
        print(n)
