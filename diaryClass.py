class Diary:
    """旅游日记类"""

    def __init__(self, user, location, images=None, videos=None):
        """
        初始化旅游日记
        :param user: 发布日记的用户对象（Account）
        :param location: 旅游的景点名
        :param images: 图片列表
        :param videos: 视频列表
        """
        self.user = user  # 关联的用户对象
        self.username = user.name  # 记录日记的用户名
        self.location = location  # 景点名
        self.images = images if images else []  # 图片路径或 URL 列表
        self.videos = videos if videos else []  # 视频路径或 URL 列表
        self.views = 0  # 浏览量（热度）
        self.ratings = []  # 评分列表
        self.rank = 0  # 排名（根据热度排序）

        # 将日记加入用户账户
        user.add_diary(self)

    def add_view(self):
        """增加浏览量"""
        self.views += 1

    def add_rating(self, rating):
        """添加评分"""
        if 0 <= rating <= 5:
            self.ratings.append(rating)

    def get_average_rating(self):
        """计算平均评分"""
        return sum(self.ratings) / len(self.ratings) if self.ratings else 0

    '''
    这里应该加一个图片和视频的url链接，以便载入
    '''

    def to_dict(self):
        """返回日记信息"""
        return {
            "username": self.username,
            "location": self.location,
            "views": self.views,
            "average_rating": self.get_average_rating(),
            "rank": self.rank,
            "images": self.images,
            "videos": self.videos
        }
