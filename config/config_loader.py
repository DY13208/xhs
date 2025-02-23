from ruamel.yaml import YAML
import os
import re

class ConfigLoader:
    def __init__(self, config_file='./config/config.yaml', sensitive_words_file='config/sensitive_words.txt'):
        self.config_file = config_file
        self.sensitive_words_file = sensitive_words_file
        self.config = None
        self.sensitive_words = []
        self.yaml = YAML()
        self.yaml.preserve_quotes = True  # 保留引号信息

    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                self.config = self.yaml.load(file)
                print("[INFO] 成功加载配置文件 config.yaml")
        except FileNotFoundError:
            print(f"[ERROR] 配置文件 {self.config_file} 未找到，请检查路径！")
        except Exception as e:
            print(f"[ERROR] 解析配置文件失败：{e}")

    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as file:
                self.yaml.dump(self.config, file)
                print(f"[INFO] 配置文件已保存到 {self.config_file}")
        except Exception as e:
            print(f"[ERROR] 保存配置文件失败：{e}")

    def load_sensitive_words(self):
        """加载敏感词库"""
        try:
            with open(self.sensitive_words_file, 'r', encoding='utf-8') as file:
                self.sensitive_words = [line.strip() for line in file if line.strip()]
                print(f"[INFO] 成功加载敏感词库，共 {len(self.sensitive_words)} 个词")
        except FileNotFoundError:
            print(f"[ERROR] 敏感词库文件 {self.sensitive_words_file} 未找到，请检查路径！")

    def get_config(self):
        """返回加载后的配置字典"""
        return self.config

    def get_sensitive_words(self):
        """返回敏感词列表"""
        return self.sensitive_words

    def _parse_key_path(self, key_path):
        """
        将形如 "accounts[0].phone" 的键路径解析为列表，例如 ["accounts", 0, "phone"]
        """
        tokens = re.findall(r'([^\.\[\]]+)', key_path)
        parsed_tokens = []
        for token in tokens:
            if token.isdigit():
                parsed_tokens.append(int(token))
            else:
                parsed_tokens.append(token)
        return parsed_tokens

    def get_value(self, key_path, default=None):
        """
        通用方法：获取配置文件中的值，支持类似 'accounts[0].phone' 的键路径
        """
        tokens = self._parse_key_path(key_path)
        current = self.config
        try:
            for token in tokens:
                current = current[token]
            return current
        except (KeyError, IndexError, TypeError):
            print(f"[WARN] 无法找到键路径: {key_path}，返回默认值: {default}")
            return default

    def set_value(self, key_path, value):
        """
        通用方法：设置配置文件中的值并保存
        注意：该方法要求键路径中涉及的结构必须已存在，否则将提示错误，
        以避免整体配置结构被意外改变。
        """
        tokens = self._parse_key_path(key_path)
        current = self.config
        # 遍历到倒数第二个 token
        for i, token in enumerate(tokens[:-1]):
            if isinstance(token, int):
                if not isinstance(current, list):
                    print(f"[ERROR] 预期 token '{token}' 为列表索引，但当前结构不是列表。")
                    return
                if token >= len(current):
                    print(f"[ERROR] 列表索引 {token} 超出范围。")
                    return
                current = current[token]
            else:
                if token not in current:
                    print(f"[ERROR] 键 '{token}' 不存在，无法设置值。请确认配置结构是否正确。")
                    return
                if not isinstance(current[token], (dict, list)) and i != len(tokens)-2:
                    print(f"[ERROR] 键 '{token}' 对应的值不是字典或列表，无法深入设置。")
                    return
                current = current[token]
        # 设置最后一个 token 的值
        last_token = tokens[-1]
        if isinstance(last_token, int):
            if not isinstance(current, list):
                print(f"[ERROR] 预期最后 token 为列表索引，但当前结构不是列表。")
                return
            if last_token >= len(current):
                print(f"[ERROR] 列表索引 {last_token} 超出范围。")
                return
            current[last_token] = value
        else:
            current[last_token] = value
        self.save_config()
        print(f"[INFO] 已成功设置 '{key_path}' 的值为：{value}")

# 调试代码：运行时可以确认配置是否正确加载和修改
if __name__ == "__main__":
    loader = ConfigLoader()
    loader.load_config()
    loader.load_sensitive_words()

    print("\n=== 配置内容 ===")
    print(loader.get_config())

    print("\n=== 敏感词列表 ===")
    print(loader.get_sensitive_words())

    # 示例：获取配置中的手机号（要求 accounts 数组及其元素已存在）
    print("\n=== 当前手机号 ===")
    print(loader.get_value("accounts[0].phone"))

    # 示例：修改手机号并保存
    # loader.set_value("accounts[0].phone", "19999999999")

    # # 示例：修改数据库主机地址
    # loader.set_value("database.host", "192.168.1.1")
    #
    # # 示例：获取数据库主机地址
    # print("\n=== 数据库主机地址 ===")
    # print(loader.get_value("database.host"))

    # 示例：获取 cookies 值（保留引号信息）
    print("\n=== 当前 cookies 值 ===")
    print(loader.get_value("accounts[1].cookies"))
