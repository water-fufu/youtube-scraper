import logging
import os

def get_logger():
    # 日志基础配置
    logger = logging.getLogger("youtube_scraper")
    logger.setLevel(logging.INFO)
    # 避免重复添加handler
    if logger.handlers:
        return logger

    # 日志格式：时间-级别-信息
    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # 1. 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # 2. 文件输出，日志保存到logs文件夹
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = logging.FileHandler("logs/scraper.log", encoding="utf-8")
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger

# 全局日志实例
log = get_logger()