# tests/test_user_service.py
import os
import json
import tempfile
import unittest

# 导入要测试的模块和函数
from app.services import user_service
from app.config import USERS_FILE

class TestUserService(unittest.TestCase):
    def setUp(self):
        """
        在每个测试方法运行之前调用，创建一个临时用户数据文件，避免污染正式数据
        """
        # 创建临时文件替代正式文件
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        # 将正式配置中的 USERS_FILE 路径临时指向该文件
        self.original_users_file = USERS_FILE
        # 注意：这里你可能需要通过某种方式让 user_service 使用新的文件路径，
        # 例如通过配置文件或环境变量传入 USERS_FILE 的路径
        # 此处仅作为示例，假设 user_service 直接读取 USERS_FILE 变量
        import app.config as config
        config.USERS_FILE = self.temp_file.name

    def tearDown(self):
        """
        每个测试方法结束后调用，清理临时文件
        """
        os.unlink(self.temp_file.name)
        # 恢复原 USERS_FILE 配置（根据实际情况操作）
        import app.config as config
        config.USERS_FILE = self.original_users_file

    def test_register_and_login(self):
        # 测试注册是否成功
        res = user_service.register("alice", "password123")
        self.assertTrue(res, "注册新用户应返回 True")
        
        # 重复注册同一用户应失败
        res = user_service.register("alice", "password123")
        self.assertFalse(res, "同一用户重复注册应返回 False")

        # 读取用户文件确认数据写入
        with open(self.temp_file.name, "r", encoding="utf-8") as f:
            users = json.load(f)
        self.assertIn("alice", users)

        # 测试登录成功
        token = user_service.login("alice", "password123")
        self.assertIsNotNone(token, "正确的密码登录应返回 token")

        # 测试使用错误密码登录应失败
        token_fail = user_service.login("alice", "wrongpass")
        self.assertIsNone(token_fail, "错误的密码登录应返回 None")

if __name__ == "__main__":
    unittest.main()
