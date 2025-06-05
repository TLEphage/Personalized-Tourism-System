import math
import heapq
import random
from app.config import MAP_FILE, INDOOR_FILE, INDOOR_CACHE_FILE
from utils.file_utils import read_json, write_json
from app.models.map import *
from algorithm.Sort import quick_sort
from algorithm.ShortestPath import dijkstra, astar

def get_map():
    graph = read_json(MAP_FILE, default={})
    return graph

def search_node(name: str):
    map_data = get_map()
    nodes = map_data.get("nodes",[])
    node_list=[]
    for node in nodes:
        if name == "__all__" or name in node.get("name",""):
            node_list.append(node.get("name",""))
    return node_list[:10]

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

def build_graph(nodes, edges, traffic_mode):
    """构建距离/时间邻接表"""
    graph = {}
    for node in nodes:
        graph[node['id']] = []
    
    for edge in edges:
        # 为每条边生成随机拥挤度 (0.8~1.0)
        crowd = random.uniform(0.8, 1.0)
        u, v = edge['start_node'], edge['end_node']
        
        if traffic_mode == 'walk':
            if edge['walk_speed'] > 0:
                time = edge['distance'] / (crowd * edge['walk_speed'])
                graph[u].append((v, time, "walk"))
                graph[v].append((u, time, "walk"))
        elif traffic_mode == 'bike':
            if edge['bike_speed'] > 0:
                time = edge['distance'] / (crowd * edge['bike_speed'])
                graph[u].append((v, time, "bike"))
                graph[v].append((u, time, "bike"))
        elif traffic_mode == 'ebike':
            if edge['ebike_speed'] > 0:
                time = edge['distance'] / (crowd * edge['ebike_speed'])
                graph[u].append((v, time, "ebike"))
                graph[v].append((u, time, "ebike"))
        elif traffic_mode == 'walk_bike':
            if edge['walk_speed'] > 0:
                time = edge['distance'] / (crowd * edge['walk_speed'])
                graph[u].append((v, time, "walk"))
                graph[v].append((u, time, "walk"))
            if edge['bike_speed'] > 0:
                time = edge['distance'] / (crowd * edge['bike_speed'])
                graph[u].append((v, time, "bike"))
                graph[v].append((u, time, "bike"))
        elif traffic_mode == 'walk_ebike':
            if edge['walk_speed'] > 0:
                time = edge['distance'] / (crowd * edge['walk_speed'])
                graph[u].append((v, time, "walk"))
                graph[v].append((u, time, "walk"))
            if edge['ebike_speed'] > 0:
                time = edge['distance'] / (crowd * edge['ebike_speed'])
                graph[u].append((v, time, "ebike"))
                graph[v].append((u, time, "ebike"))
        else:
            distance=edge['distance']
            graph[u].append((v,distance, traffic_mode))
            graph[v].append((u,distance, traffic_mode))
    
    return graph

def get_node_by_id(nodes_dict, node_id):
    """根据ID查找节点信息"""
    return nodes_dict[node_id]

def one_to_one_shortest_path(start_name, end_name):
    """一到一最短路查询"""
    map_data = get_map()
    nodes = map_data['nodes']
    edges = map_data['edges']
    nodes_dict = {}
    for node in nodes:
        nodes_dict[node.get('id',0)]=node    
    start_id = next((node['id'] for node in nodes if node['name'] == start_name), -1)
    end_id = next((node['id'] for node in nodes if node['name'] == end_name), -1)

    if start_id == -1 or end_id == -1:
        raise("地点不存在")
    # 构建邻接表
    graph = build_graph(nodes, edges, "no traffic mode")
    
    # 预处理启发式函数（欧氏距离）
    end_node = get_node_by_id(nodes_dict, end_id)
    heuristic = lambda node_id: haversine(
        get_node_by_id(nodes_dict, node_id)['latitude'],
        get_node_by_id(nodes_dict, node_id)['longitude'],
        end_node['latitude'],
        end_node['longitude']
    )
    
    # 调用A*算法
    path_node_ids, total_distance = astar(start_id, end_id, graph, heuristic)
    
    # 获取完整节点信息
    path_nodes = [get_node_by_id(nodes_dict, node_id) for node_id in path_node_ids]
    
    return path_nodes, round(total_distance,2)

def one_to_one_shortest_time(start_name, end_name, traffic_mode="walk"):
    """一到一最短时间查询"""
    map_data = get_map()
    nodes = map_data['nodes']
    edges = map_data['edges']
    nodes_dict = {}
    for node in nodes:
        nodes_dict[node.get('id',0)]=node   

    start_id = next((node['id'] for node in nodes if node['name'] == start_name), -1)
    end_id = next((node['id'] for node in nodes if node['name'] == end_name), -1)
    
    if start_id == -1 or end_id == -1:
        raise("地点不存在")
    # 构建邻接表
    graph = build_graph(nodes, edges, traffic_mode)
    
    # 调用Dijkstra算法
    path_node_ids, total_time = dijkstra(start_id, {end_id}, graph)
    
    # 计算实际移动距离（使用原始距离）
    total_distance = 0.0
    for i in range(len(path_node_ids) - 1):
        u, v = get_node_by_id(nodes_dict, path_node_ids[i]), get_node_by_id(nodes_dict, path_node_ids[i+1])
        total_distance += haversine(u['latitude'],u['longitude'],v['latitude'],v['longitude'])
    
    # 获取从该点出发使用的交通方式
    path_mode = []
    for i in range(len(path_node_ids) - 1):
        u, v = path_node_ids[i], path_node_ids[i+1]
        minimun_time = float('inf')
        mode_select = "walk"
        for node, time, mode in graph[u]:
            if node == v and time < minimun_time:
                minimun_time = time
                mode_select = mode
        path_mode.append(mode_select)

    # 获取完整节点信息
    path_nodes = [get_node_by_id(nodes_dict, node_id) for node_id in path_node_ids]
    
    return path_nodes, path_mode, round(total_time,2), round(total_distance,2)

def one_to_many_shortest_path(start_name, target_names):
    """一到多最短路径查询"""
    map_data = get_map()
    nodes = map_data['nodes']
    edges = map_data['edges']
    nodes_dict = {}
    for node in nodes:
        nodes_dict[node.get('id',0)]=node   
        
    start_id = next((node['id'] for node in nodes if node['name'] == start_name), -1)
    if start_id == -1:
        raise("地点不存在")
    target_ids=[]
    for end_name in target_names:
        end_id = next((node['id'] for node in nodes if node['name'] == end_name), -1)
        if end_id == -1:
            raise ValueError("有不存在的目的地")
        target_ids.append(end_id)
    
    # 构建邻接表
    graph = build_graph(nodes, edges, "no traffic mode")
    
    current = start_id
    remaining_targets = set(target_ids)
    full_path = [start_id]
    total_distance = 0.0
    
    # 依次访问所有目标点
    while remaining_targets:
        # 找到最近的目标点
        path_segment, dist = dijkstra(current, remaining_targets, graph)
        
        if not path_segment:
            break
        
        # 更新路径和距离
        full_path.extend(path_segment[1:])  # 避免重复添加当前点
        total_distance += dist
        current = path_segment[-1]
        remaining_targets.discard(current)
    
    # 从最后一个目标点回到起点
    if full_path[-1] != start_id:
        return_path, return_dist = dijkstra(current, {start_id}, graph)
        if return_path:
            full_path.extend(return_path[1:])
            total_distance += return_dist
    
    # 获取完整节点信息
    full_path_nodes = [get_node_by_id(nodes_dict, node_id) for node_id in full_path]
    
    return full_path_nodes, round(total_distance,2)

def indoor_shortest_path(start_name, end_name):
    indoor_cache = {
            "1L":{"path": [], "distance": 0},
            "2L":{"path": [], "distance": 0},
            "3L":{"path": [], "distance": 0},
        }
    write_json(INDOOR_CACHE_FILE, indoor_cache)
    map_data = read_json(INDOOR_FILE, default={})
    nodes = map_data.get("nodes",[])
    edges = map_data.get("edges",[])
    start_node={}
    end_node={}
    graph = build_graph(nodes, edges, "no traffic mode")
    for node in nodes:
        if node['name']==start_name:
            start_node=node
        if node['name']==end_name:
            end_node=node
    if not start_node or not end_node:
        raise ValueError("地点不存在")
    
    if start_node['floor'] == end_node['floor']:
        # 可优化部分：减少节点数
        # n_nodes = [node for node in nodes if node.get("floor") == start_node['floor']]
        
        path, distance = dijkstra(start_node['id'], {end_node['id']}, graph)
        indoor_cache[start_node['floor']]["path"]=path
        indoor_cache[start_node['floor']]["distance"]=distance
        write_json(INDOOR_CACHE_FILE, indoor_cache)
        return {"success": True}
    elevator1={}
    elevator2={}
    for node in nodes:
        if node['floor'] == start_node['floor'] and node['type']=='电梯':
            elevator1=node
        if node['floor'] == end_node['floor'] and node['type']=='电梯':
            elevator2=node
    if not elevator1 or not elevator2:
        return ValueError("找不到路径")
    path, distance = dijkstra(start_node['id'], {elevator1['id']}, graph)
    indoor_cache[start_node['floor']]["path"]=path
    indoor_cache[start_node['floor']]["distance"]=distance   
    path, distance = dijkstra(elevator2['id'], {end_node['id']}, graph)
    indoor_cache[end_node['floor']]["path"]=path
    indoor_cache[end_node['floor']]["distance"]=distance   
    write_json(INDOOR_CACHE_FILE, indoor_cache)
    return {"success": True}

def get_indoor_path(floor: str):
    data = read_json(INDOOR_CACHE_FILE)
    if floor not in data:
        raise ValueError("楼层不存在")
    return data[floor]["path"], data[floor]["distance"]

def add_node(node_data: NodeRequest) -> dict:
    """将请求的节点加入地图数据中"""
    graph = get_map()
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
    graph = get_map()
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
        'distance' : round(haversine(lat1, lon1, lat2, lon2), 2),
        'walk_speed' : edge_data.walk_speed,
        'bike_speed' : edge_data.bike_speed,
        'ebike_speed' : edge_data.ebike_speed
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

from algorithm.Hash import simple_hash

def _load_places():
    global head_index
    global next_index
    graph = get_map()
    nodes = graph.get('nodes', [])
    head_index=[]
    next_index=[-1]*len(nodes)

    data=[]
    for i in range(len(nodes)):
        hash_value = simple_hash(nodes[i].get("type",""))
        data.append((hash_value,i))
    data.sort(key=lambda x: x[0])
    for i in range(len(data)):
        if i==0 or data[i][0]!=data[i-1][0]:
            head_index.append((data[i][1],data[i][0]))
        else:
            next_index[data[i-1][1]]=data[i][1]

_load_places()

def search_places(longitude: float, latitude: float, query_type: str, max_results: int, max_distance: float):
    """查询最近的指定类型节点"""
    graph = get_map()
    nodes = graph.get('nodes', [])
    candidates = []

    hash_value = simple_hash(query_type)
    for index, value in head_index:
        if hash_value==value:
            while index != -1:
                node=nodes[index]
                lon1=longitude
                lat1=latitude
                lon2=node.get('longitude')
                lat2=node.get('latitude')
                distance=round(haversine(lat1, lon1, lat2, lon2), 2)
                if distance <= max_distance:
                    candidate_node = PlaceDetail(
                        id=node.get('id'),
                        name=node.get('name'),
                        type=node.get('type'),
                        popularity=node.get('popularity'),
                        longitude=node.get('longitude'),
                        latitude=node.get('latitude'),
                        distance=distance
                    )
                    candidates.append(candidate_node)
                index=next_index[index]
            break
            
    sorted_places = quick_sort(candidates, sort_key=lambda x: x.distance)
    return sorted_places[:max_results]

# 示例调用
if __name__ == '__main__':
    path, distance= one_to_one_shortest_path("北门", "西门")
    print(path)
    print(distance)

    path, mode, time, distance = one_to_one_shortest_time("北门", "学六公寓", "walk_ebike")
    print(path)
    print(mode)
    print(time)
    print(distance)

    path, distance= one_to_many_shortest_path("北门", ["西门","东门"])
    print(path)
    print(distance)
    # print(f"距离：{distance}, 花费: {time} 分钟")
    # print("路径:")
    # for n in path:
    #     print(n)
