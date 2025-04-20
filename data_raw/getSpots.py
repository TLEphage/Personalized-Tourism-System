import requests
import json
import time

API_KEY = "b53e7b3d0d439b55ab743f24df3c232d"  # 替换为你的高德 Key
SEARCH_URL = "https://restapi.amap.com/v5/place/text"

def parse_poi(poi):
    """将单条 POI JSON 转为目标字段格式"""
    loc = poi.get("location", "").split(",")
    rec = poi.get("recommend_info", {}) or {}
    return {
        "name": poi.get("name", ""),
        "description": rec.get("intro", "暂无描述"),
        "location": poi.get("address", ""),
        "coordinates": {
            "longitude": float(loc[0]) if len(loc) == 2 else None,
            "latitude":  float(loc[1]) if len(loc) == 2 else None
        },
        "rating": float(poi.get("rating", 0)),
        "popularity": int(rec.get("score", 0)),
        "tags": poi.get("tag", "").split(";") if poi.get("tag") else [],
        "price_range": poi.get("cost", "免费"),
        "open_hours": poi.get("open_time", {})
    }

def get_top200_china_spots():
    all_pois = []
    seen_ids = set()
    params = {
        "key": API_KEY,
        "keywords": "景点",
        "extensions": "all",
        "show_fields": "rating,cost,tag,open_time,recommend_info",
        "citylimit": "false",
        "page_size": 25,  # 接口最大25条
        "page_num": 1
    }

    while len(all_pois) < 200:
        resp = requests.get(SEARCH_URL, params=params, timeout=10)
        data = resp.json()
        pois = data.get("pois", [])
        if not pois:
            break  # 没有更多数据

        for poi in pois:
            poi_id = poi.get("id")
            if not poi_id or poi_id in seen_ids:
                continue
            seen_ids.add(poi_id)
            all_pois.append(parse_poi(poi))
            if len(all_pois) >= 200:
                break

        if len(pois) < params["page_size"]:
            break  # 当前页不足，数据取尽
        params["page_num"] += 1
        time.sleep(0.2)  # 避免限流

    # 按热度降序取前200
    all_pois.sort(key=lambda x: x["popularity"], reverse=True)
    return all_pois[:200]

def save_to_json(spots, filename="china_top200_spots.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"scenic_spots": spots}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    spots = get_top200_china_spots()
    save_to_json(spots)
    print(f"已获取并保存中国热度前{len(spots)}的景点至 china_top200_spots.json")
