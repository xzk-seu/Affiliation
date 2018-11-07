import logging


def get_logger(level=logging.INFO):
    logger = logging.getLogger()  # 不加名称设置root logger
    logger.setLevel(level=level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    # 使用StreamHandler输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(level=level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # 使用FileHandler输出到文件, 文件默认level:ERROR
    fh = logging.FileHandler('log')
    fh.setLevel(level=logging.ERROR)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


logger = get_logger()
