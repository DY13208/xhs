from database.xhs_database import SessionLocal
from database.models import LogEntry
from core.utils.logger import logger

def save_log(account_id, operation_type, status, message):
    """保存操作日志到数据库"""
    session = SessionLocal()
    try:
        log_entry = LogEntry(
            account_id=account_id,
            operation_type=operation_type,
            status=status,
            message=message
        )
        session.add(log_entry)
        session.commit()
        logger.info(f"日志保存成功：{log_entry}")
    except Exception as e:
        logger.error(f"日志保存失败：{e}")
    finally:
        session.close()
