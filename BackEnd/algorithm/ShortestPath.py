import heapq
import math
from collections import defaultdict

def dijkstra(start, targets, graph):
    """
    使用Dijkstra算法计算从起点到目标集合中任意一点的最短路径
    参数:
        start: 起点节点ID
        targets: 目标节点ID集合
        graph: 邻接表 {node: [(neighbor, weight, mode)]}
    返回:
        path: 节点ID列表 (从起点到终点)
        total_cost: 路径总长度
    """
    if start in targets:
        return [start], 0.0

    # 初始化数据结构
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0.0
    prev = {}
    pq = [(0.0, start)]
    
    while pq:
        cost, node = heapq.heappop(pq)
        if node in targets:
            # 构建路径
            path = []
            while node != start:
                path.append(node)
                node = prev[node]
            path.append(start)
            return path[::-1], cost
        
        if cost > dist[node]:
            continue
            
        for neighbor, weight, __  in graph[node]:
            new_cost = cost + weight
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                prev[neighbor] = node
                heapq.heappush(pq, (new_cost, neighbor))
    
    return [], float('inf')

def astar(start, end, graph, heuristic):
    """
    使用A*算法计算从起点到终点的最短路径
    参数:
        start: 起点节点ID
        end: 终点节点ID
        graph: 邻接表 {node: [(neighbor, weight, mode)]}
        heuristic: 启发式函数 {node: 到终点的估计距离}
    返回:
        path: 节点ID列表 (从起点到终点)
        total_cost: 路径总长度
    """
    if start == end:
        return [start], 0.0

    # 初始化数据结构
    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0.0
    f_score = defaultdict(lambda: float('inf'))
    f_score[start] = heuristic(start)
    prev = {}
    pq = [(f_score[start], start)]
    
    while pq:
        _, node = heapq.heappop(pq)
        if node == end:
            # 构建路径
            path = []
            while node != start:
                path.append(node)
                node = prev[node]
            path.append(start)
            return path[::-1], g_score[end]
        
        for neighbor, weight, __ in graph[node]:
            tentative_g = g_score[node] + weight
            if tentative_g < g_score[neighbor]:
                prev[neighbor] = node
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor)
                heapq.heappush(pq, (f_score[neighbor], neighbor))
    
    return [], float('inf')