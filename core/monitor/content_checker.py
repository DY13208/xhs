import re
from core.utils.logger import logger

class ContentChecker:
    """内容违规检测模块"""

    def __init__(self, sensitive_words_file="config/sensitive_words.txt"):
        self.sensitive_words = self.load_sensitive_words(sensitive_words_file)

    def load_sensitive_words(self, file_path):
        """加载敏感词列表"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                words = [line.strip() for line in file if line.strip()]
            logger.info(f"成功加载 {len(words)} 个敏感词。")
            return words
        except FileNotFoundError:
            logger.error(f"敏感词文件 {file_path} 未找到。")
            return []

    def check_content(self, content):
        """检查内容是否包含敏感词"""
        for word in self.sensitive_words:
            if re.search(rf"\b{word}\b", content, re.IGNORECASE):
                logger.warning(f"检测到敏感词：{word}")
                return False
        logger.info("内容合规，无敏感词。")
        return True
