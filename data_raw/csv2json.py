import os
import json
import csv
import math

MAP_JSON = 'map.json'
NODES_CSV = 'map_node.csv'
EDGES_CSV = 'map_edge.csv'

# Haversine formula to compute distance in meters between two lat/lon points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def initialize_map():
    # Remove existing file if it exists
    if os.path.exists(MAP_JSON):
        os.remove(MAP_JSON)
    # Create empty structure
    data = {
        "nodes": [],
        "edges": []
    }
    # Write JSON with ensure_ascii=False to preserve unicode characters
    with open(MAP_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_map():
    with open(MAP_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_map(data):
    # Write JSON with ensure_ascii=False to preserve unicode characters
    with open(MAP_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add_nodes():
    data = load_map()
    existing_names = {node['name'] for node in data['nodes']}
    with open(NODES_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) != 5:
                continue
            nid, name, lon, lat, ntype = row
            if name in existing_names:
                continue
            try:
                node = {
                    "id": int(nid),
                    "name": name,
                    "type": ntype,
                    "popularity": 100,
                    "longitude": float(lon),
                    "latitude": float(lat),
                    "connected_edges": []
                }
            except ValueError:
                continue
            data['nodes'].append(node)
            existing_names.add(name)
    save_map(data)


def add_edges():
    data = load_map()
    # Build lookup of nodes by id
    node_index = {node['id']: node for node in data['nodes']}
    existing_pairs = {(edge['start_node'], edge['end_node']) for edge in data['edges']}
    with open(EDGES_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 3:
                continue
            eid, start, end = row[0], row[1], row[2]
            try:
                eid_i = int(eid)
                start_i = int(start)
                end_i = int(end)
            except ValueError:
                continue
            pair = (start_i, end_i)
            if pair in existing_pairs or (end_i, start_i) in existing_pairs:
                continue
            # Ensure nodes exist
            if start_i not in node_index or end_i not in node_index:
                continue
            node_a = node_index[start_i]
            node_b = node_index[end_i]
            # Calculate distance and round to 2 decimal places
            dist = haversine(node_a['latitude'], node_a['longitude'],
                             node_b['latitude'], node_b['longitude'])
            dist = round(dist, 2)
            edge = {
                "id": eid_i,
                "start_node": start_i,
                "end_node": end_i,
                "distance": dist,
                "walk_speed": 1.0,
                "bike_speed": 3.0,
                "ebike_speed": 0.0
            }
            data['edges'].append(edge)
            # update connected_edges for both nodes
            node_a['connected_edges'].append(eid_i)
            node_b['connected_edges'].append(eid_i)
            existing_pairs.add(pair)
    save_map(data)


def main():
    initialize_map()
    add_nodes()
    add_edges()
    final_data = load_map()
    print(f"Generated {MAP_JSON} with {len(final_data['nodes'])} nodes and {len(final_data['edges'])} edges.")

if __name__ == '__main__':
    main()
