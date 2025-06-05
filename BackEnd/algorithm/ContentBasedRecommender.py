import re
from typing import List, Dict, Set, Tuple
from collections import defaultdict, Counter
import math

class UserManager:
    """用户管理器，负责管理用户信息和爱好"""
    
    def __init__(self):
        self.users = {}  # 用户信息存储：{用户ID: {爱好集合}}
    
    def add_user(self, user_id: str, hobbies: List[str]) -> None:
        """添加新用户及其爱好"""
        self.users[user_id] = set(hobbies)
    
    def update_hobbies(self, user_id: str, hobbies: List[str]) -> None:
        """更新用户爱好"""
        if user_id in self.users:
            self.users[user_id].update(hobbies)
        else:
            self.add_user(user_id, hobbies)
    
    def get_user_hobbies(self, user_id: str) -> Set[str]:
        """获取用户爱好集合"""
        return self.users.get(user_id, set())

class DiaryDatabase:
    """日记数据库，负责存储和检索日记"""
    
    def __init__(self):
        self.diaries = []  # 存储所有日记
        self.tfidf = TfIdfCalculator()
    
    def add_diary(self, diary_id: str, content: str, tags: List[str] = None) -> None:
        """添加新日记"""
        if tags is None:
            tags = []
        
        # 提取内容中的关键词作为额外标签
        keywords = self._extract_keywords(content)
        all_tags = list(set(tags + keywords))
        
        diary = {
            "id": diary_id,
            "content": content,
            "tags": all_tags,
            "keyword_vector": self.tfidf.calculate_vector(all_tags)
        }
        
        self.diaries.append(diary)
        self.tfidf.add_document(all_tags)
    
    def _extract_keywords(self, content: str) -> List[str]:
        """从日记内容中提取关键词（简化版）"""
        # 简单的关键词提取，实际应用中可以使用更复杂的NLP方法
        words = re.findall(r'\b\w+\b', content.lower())
        # 过滤常见停用词（简化版）
        stopwords = {'the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'it', 'with'}
        keywords = [word for word in words if word not in stopwords and len(word) > 2]
        # 取最常见的5个词作为关键词
        return [word for word, _ in Counter(keywords).most_common(5)]
    
    def get_all_diaries(self) -> List[Dict]:
        """获取所有日记"""
        return self.diaries

class TfIdfCalculator:
    """TF-IDF计算器，用于计算文本相似度"""
    
    def __init__(self):
        self.document_count = 0
        self.word_document_count = defaultdict(int)  # 记录包含每个词的文档数
    
    def add_document(self, words: List[str]) -> None:
        """添加文档以更新统计信息"""
        self.document_count += 1
        unique_words = set(words)
        for word in unique_words:
            self.word_document_count[word] += 1
    
    def calculate_vector(self, words: List[str]) -> Dict[str, float]:
        """计算词向量（TF-IDF值）"""
        vector = {}
        word_counts = Counter(words)
        total_words = len(words)
        
        for word, count in word_counts.items():
            # 计算TF (词频)
            tf = count / total_words
            
            # 计算IDF (逆文档频率)
            doc_count = self.word_document_count.get(word, 0)
            if doc_count == 0:
                idf = 0
            else:
                idf = math.log(self.document_count / doc_count)
            
            # 计算TF-IDF
            vector[word] = tf * idf
        
        return vector

class DiaryRecommender:
    """日记推荐器，根据用户爱好推荐相关日记"""
    
    def __init__(self, user_manager: UserManager, diary_db: DiaryDatabase):
        self.user_manager = user_manager
        self.diary_db = diary_db
    
    def recommend_diaries(self, user_id: str, limit: int = 5) -> List[Dict]:
        """为用户推荐日记"""
        user_hobbies = self.user_manager.get_user_hobbies(user_id)
        if not user_hobbies:
            return []
        
        # 将用户爱好转换为向量
        hobby_vector = self.diary_db.tfidf.calculate_vector(list(user_hobbies))
        
        # 计算所有日记与用户爱好的相似度
        diaries = self.diary_db.get_all_diaries()
        similarity_scores = []
        
        for diary in diaries:
            score = self._cosine_similarity(hobby_vector, diary["keyword_vector"])
            similarity_scores.append((diary, score))
        
        # 按相似度排序并返回前limit个日记
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        return [diary for diary, _ in similarity_scores[:limit]]
    
    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """计算两个向量的余弦相似度"""
        dot_product = 0
        vec1_norm = 0
        vec2_norm = 0
        
        # 计算点积
        for word in set(vec1.keys()) & set(vec2.keys()):
            dot_product += vec1[word] * vec2[word]
        
        # 计算向量1的范数
        for value in vec1.values():
            vec1_norm += value ** 2
        vec1_norm = math.sqrt(vec1_norm)
        
        # 计算向量2的范数
        for value in vec2.values():
            vec2_norm += value ** 2
        vec2_norm = math.sqrt(vec2_norm)
        
        # 计算余弦相似度
        if vec1_norm == 0 or vec2_norm == 0:
            return 0
        return dot_product / (vec1_norm * vec2_norm)

# 使用示例
if __name__ == "__main__":
    # 初始化组件
    user_manager = UserManager()
    diary_db = DiaryDatabase()
    recommender = DiaryRecommender(user_manager, diary_db)
    
    # 添加用户和爱好
    user_manager.add_user("user1", ["阅读", "旅行", "摄影"])
    
    # 添加日记
    diary_db.add_diary("diary1", "今天去了一个美丽的海滩，拍了很多漂亮的照片", ["旅行", "摄影", "海滩"])
    diary_db.add_diary("diary2", "读了一本关于人工智能的好书，收获很大", ["阅读", "人工智能", "书籍"])
    diary_db.add_diary("diary3", "尝试了新的烹饪食谱，做了一顿美味的晚餐", ["烹饪", "美食"])
    diary_db.add_diary("diary4", "徒步旅行到山顶，风景美不胜收", ["旅行", "徒步", "自然"])
    diary_db.add_diary("diary5", "参加了一个摄影展览，看到了很多优秀作品", ["摄影", "艺术", "展览"])
    
    # 为用户推荐日记
    recommendations = recommender.recommend_diaries("user1", limit=3)
    
    # 输出推荐结果
    print("为您推荐的日记：")
    for i, diary in enumerate(recommendations, 1):
        print(f"{i}. {diary['id']}: {diary['content'][:50]}... (标签: {', '.join(diary['tags'])})")    