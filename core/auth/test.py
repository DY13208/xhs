from config.config_loader import ConfigLoader
from core.auth.account_manager import AccountManager

# 加载配置
config_loader = ConfigLoader()
config_loader.load_config()
accounts = config_loader.get_config().get("accounts", [])

# 初始化多账号管理器并登录
account_manager = AccountManager(accounts)
account_manager.login_all_accounts()

# 获取某个账号的客户端
client = account_manager.get_client("account1")
if client:
    client.get_account_info()
