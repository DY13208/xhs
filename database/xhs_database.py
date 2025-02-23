from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yaml

# 从 config.yaml 读取数据库配置
def load_db_config():
    with open("config/config.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config["database"]

# 数据库连接初始化
db_config = load_db_config()
DB_URL = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?charset=utf8mb4"

# 创建数据库引擎和会话
engine = create_engine(DB_URL, echo=True)  # echo=True 会输出 SQL 语句到控制台
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
