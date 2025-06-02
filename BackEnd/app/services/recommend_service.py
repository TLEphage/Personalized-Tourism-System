# app/services/recommendation_service.py
from utils.file_utils import read_json,read_compressed_json
from app.config import USERS_FILE, SPOTS_FILE, FOODS_FILE, DIARIES_FILE

# 计算匹配得分：tags 匹配得 2 分，文本字段匹配得 1 分

def compute_match_score(hobbies, text_fields, tags):
    score = 0
    for hobby in hobbies:
        if tags and any(hobby in tag for tag in tags):
            score += 2
        for field in text_fields:
            if field and hobby in field:
                score += 1
    return score

# 各类别推荐权重设置：
# scenic_spots: match_norm * 0.7 + rating * 0.1 + popularity * 0.2
# schools:     match_norm * 0.5 + rating * 0.2 + popularity * 0.3
# foods:       match_norm * 0.7 + rating * 0.2 + popularity * 0.1
# diaries:     match_norm * 0.6 + rating * 0.1 + views * 0.3

CATEGORY_WEIGHTS = {
    "scenic_spot": {
        "match": 0.7,
        "rating": 0.1,
        "popularity": 0.2
    },
    "school": {
        "match": 0.5,
        "rating": 0.2,
        "popularity": 0.3
    },
    "food": {
        "match": 0.7,
        "rating": 0.2,
        "popularity": 0.1
    },
    "diary": {
        "match": 0.6,
        "rating": 0.1,
        "popularity": 0.3  # 使用 views 作为热度指标
    }
}

# 计算最终推荐分数，将各组件归一化后加权

def compute_final_score(item_type, match_norm, rating=None, popularity=None, views=None):
    weights = CATEGORY_WEIGHTS.get(item_type)
    if not weights:
        return 0
    # 对 rating、popularity、views 做简单归一化：假设 rating 最大 5 分，popularity 最大 100，views 最大 100
    norm_rating = rating / 5 if rating is not None else 0
    norm_popularity = popularity / 100 if popularity is not None else 0
    norm_views = views / 100 if views is not None else 0

    score = 0
    score += weights["match"] * match_norm
    # 根据类型添加对应指标
    if item_type in ["scenic_spot", "school", "food"]:
        score += weights["rating"] * norm_rating
        score += weights["popularity"] * norm_popularity
    elif item_type == "diary":
        score += weights["rating"] * norm_rating
        score += weights["popularity"] * norm_views
    return score


def recommend_for_user(username):
    users = read_json(USERS_FILE, default=[])
    user = next((u for u in users if u["username"] == username), None)
    if not user:
        raise ValueError(f"未找到用户名 {username} ")

    hobbies = user.get("hobbies", [])
    hobby_count = len(hobbies)
    max_match_per_hobby = 4  # 每个兴趣点最多：tags(2) + 文本(2)
    max_match_total = hobby_count * max_match_per_hobby if hobby_count > 0 else 1

    # 加载地点数据
    spots_data = read_json(SPOTS_FILE, default={})
    schools = spots_data.get("schools", [])
    scenic_spots = spots_data.get("scenic_spots", [])
    spot_recommendations = []

    # 推荐学校
    for school in schools:
        raw_match = compute_match_score(hobbies, [school.get("name", ""), school.get("description", "")], school.get("tags", []))
        
        match_norm = raw_match / max_match_total
        rating = school.get("rating", 0)
        popularity = school.get("popularity", 0)
        final_score = compute_final_score("school", match_norm, rating=rating, popularity=popularity)
        spot_recommendations.append({"item": school, "match_score": round(match_norm*100, 2), "final_score": round(final_score*100,2), "type": "school"})

    # 推荐景点
    for spot in scenic_spots:
        raw_match = compute_match_score(hobbies, [spot.get("name", ""), spot.get("description", "")], spot.get("tags", []))
        
        match_norm = raw_match / max_match_total
        rating = spot.get("rating", 0)
        popularity = spot.get("popularity", 0)
        final_score = compute_final_score("scenic_spot", match_norm, rating=rating, popularity=popularity)
        spot_recommendations.append({"item": spot, "match_score": round(match_norm*100,2), "final_score": round(final_score*100,2), "type": "scenic_spot"})

    # 加载美食数据
    foods_data = read_json(FOODS_FILE, default={})
    foods = foods_data.get("foods", [])
    food_recommendations = []
    for food in foods:
        raw_match = compute_match_score(hobbies, [food.get("restaurant_name", ""), food.get("description", "")], food.get("tags", []))
        
        match_norm = raw_match / max_match_total
        rating = food.get("rating", 0)
        popularity = food.get("popularity", 0)
        final_score = compute_final_score("food", match_norm, rating=rating, popularity=popularity)
        food_recommendations.append({"item": food, "match_score": round(match_norm*100,2), "final_score": round(final_score*100,2)})

    # 加载日记数据
    diaries = read_compressed_json(DIARIES_FILE, default=[])
    diary_recommendations = []
    for diary in diaries:
        raw_match = compute_match_score(hobbies, [diary.get("title", ""), diary.get("content", "")], diary.get("tags", []))
        
        match_norm = raw_match / max_match_total
        rating = diary.get("rating", 0)
        views = diary.get("views", 0)
        final_score = compute_final_score("diary", match_norm, rating=rating, views=views)
        diary_recommendations.append({"item": diary, "match_score": round(match_norm*100,2), "final_score": round(final_score*100,2)})

    return {
        "schools": sorted([r for r in spot_recommendations if r["type"] == "school"], key=lambda x: x["final_score"], reverse=True)[:10],
        "scenic_spots": sorted([r for r in spot_recommendations if r["type"] == "scenic_spot"], key=lambda x: x["final_score"], reverse=True)[:10],
        "foods": sorted(food_recommendations, key=lambda x: x["final_score"], reverse=True)[:10],
        "diaries": sorted(diary_recommendations, key=lambda x: x["final_score"], reverse=True)[:10]
    }
