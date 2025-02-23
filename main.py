import time

from config.config_loader import ConfigLoader
from core.auth.xhs_client import XHSClient
from core.automator.activity_engine import ActivityEngine
from core.automator.publish_engine import PublishEngine
from core.monitor.content_checker import ContentChecker
from core.monitor.risk_detector import RiskDetector
from core.utils.logger import logger
from tasks.task_scheduler import schedule_tasks


def main():
    # 1. 加载配置文件与敏感词库
    config_loader = ConfigLoader(config_file="config/config.yaml", sensitive_words_file="config/sensitive_words.txt")
    config_loader.load_config()
    config_loader.load_sensitive_words()
    config = config_loader.get_config()
    logger.info("配置文件加载成功。")

    # 检查配置中是否存在 account 配置
    if "account" not in config:
        logger.error("配置文件中缺少 'account' 配置，请检查配置文件。")
        return

    # 2. 初始化小红书客户端（单账号）
    account = config["account"]
    client = XHSClient(username=account["username"], password=account["password"])

    if client.login():
        logger.info(f"账号 {account['username']} 登录成功。")
    else:
        logger.error(f"账号 {account['username']} 登录失败，程序退出。")
        return

    # 3. 初始化自动化、监控模块
    activity_engine = ActivityEngine(client)
    publish_engine = PublishEngine(client)
    content_checker = ContentChecker()
    risk_detector = RiskDetector(client)

    # 4. 执行活跃操作（模拟点赞/评论/收藏）
    logger.info("开始执行活跃操作...")
    note_ids = ["note1", "note2", "note3"]  # 示例笔记 ID 列表
    for note_id in note_ids:
        risk_detector.check_operation_frequency()
        risk_detector.simulate_human_behavior()
        activity_engine.like_notes([note_id])

    # 5. 启动定时任务调度（用于定时发布笔记等任务）
    logger.info("启动定时任务调度...")
    schedule_tasks()

    # 6. 保持主程序运行，等待定时任务触发
    try:
        while True:
            time.sleep(60)  # 每 60 秒检查一次任务状态
    except KeyboardInterrupt:
        logger.info("程序已手动停止。")


if __name__ == "__main__":
    main()
