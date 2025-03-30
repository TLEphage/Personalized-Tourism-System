class Account:
    def __init__(self,name,student_id,password,interests=None):
        """
                初始化用户账户
                :param name: 用户姓名
                :param student_id: 学号
                :param password: 登录密码
                :param interests: 个人兴趣（列表）
                """
        self.name=name
        self.student_id=student_id
        self.password=password
        self.interests=interests if interests else []
        self.diaries = []  # 该用户发布的日记列表

    def add_diary(self, diary):
        """将日记添加到用户账户"""
        self.diaries.append(diary)

    def get_diaries(self):
        """获取该用户的所有日记"""
        return [diary.to_dict() for diary in self.diaries]

    def to_dict(self):
        """返回用户信息（不包含密码）"""
        return {
            "name": self.name,
            "student_id": self.student_id,
            "interests": self.interests,
            "diaries": [diary.to_dict() for diary in self.diaries]
        }







