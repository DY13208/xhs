from core.auth.xhs_client import XHSClient
from core.utils.logger import logger
import time
import random


class AccountManager:
    """多账号管理系统"""

    def __init__(self, accounts):
        self.accounts = accounts
        self.active_client = None

    def rotate_account(self):
        """轮换账号"""
        if self.active_client:
            self.active_client.close()

        account = random.choice(self.accounts)
        logger.info(f"正在切换到账号：{account['username']}")

        client = XHSClient(account)
        client.login()

        if client.is_logged_in:
            self.active_client = client
            logger.info(f"账号 {account['username']} 已启用。")
        else:
            logger.error(f"账号 {account['username']} 启用失败。")

    def get_active_client(self):
        """获取当前活动账号的客户端"""
        if not self.active_client:
            self.rotate_account()
        return self.active_client
