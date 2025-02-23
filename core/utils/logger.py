import logging
import os
from logging.handlers import RotatingFileHandler

# 创建日志目录
if not os.path.exists("logs"):
    os.makedirs("logs")


def setup_logger(name="xiaohongshu_bot", log_file="logs/bot.log", level=logging.INFO):
    """设置日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 创建文件处理器（日志文件大小限制为 5MB，最多保留 5 个历史文件）
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# 全局日志对象
logger = setup_logger()
