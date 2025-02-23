import time
import random
from core.utils.logger import logger

class RiskDetector:
    """风控检测模块"""

    def __init__(self, client):
        self.client = client
        self.operation_count = 0
        self.start_time = time.time()

    def check_operation_frequency(self, max_operations=10, time_window=3600):
        """检测操作频率，避免过于频繁"""
        current_time = time.time()
        if current_time - self.start_time > time_window:
            self.operation_count = 0
            self.start_time = current_time

        self.operation_count += 1
        if self.operation_count > max_operations:
            logger.warning("操作过于频繁，暂停一段时间以降低风险。")
            sleep_time = random.uniform(300, 600)  # 随机暂停 5-10 分钟
            time.sleep(sleep_time)
            self.operation_count = 0

    def simulate_human_behavior(self):
        """模拟人类操作行为"""
        sleep_time = random.uniform(1, 5)
        logger.info(f"模拟人类操作，暂停 {sleep_time:.2f} 秒...")
        time.sleep(sleep_time)
