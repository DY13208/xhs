from sqlalchemy import Column, Integer, String, DateTime, func
from database.xhs_database import Base

class LogEntry(Base):
    """日志模型"""
    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=func.now())
    account_id = Column(String(50), nullable=False)
    operation_type = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)
    message = Column(String(255))

    def __repr__(self):
        return f"<LogEntry(id={self.id}, account_id={self.account_id}, operation_type={self.operation_type}, status={self.status})>"
