import random
from core.utils.logger import logger

class CommentGenerator:
    """评论生成器（结合 DeepSeek 模型生成评论）"""

    def __init__(self, model):
        self.model = model

    def generate_comment(self, context):
        """根据上下文生成评论"""
        try:
            comment = self.model.generate(context)  # DeepSeek 模型调用
            logger.info(f"生成评论：{comment}")
            return comment
        except Exception as e:
            logger.error(f"生成评论失败：{e}")
            return "赞！"

    def batch_generate_comments(self, contexts):
        """批量生成评论"""
        return [self.generate_comment(context) for context in contexts]
