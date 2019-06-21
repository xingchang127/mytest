# 定义日志器并尝试封装


import logging
from scripts.handle_config import config
from scripts.constants import LOGS_FILE_PATH


class HandleLogging():
    """
    定义处理日志输出的类
    """
    def __init__(self):
        # 1.定义日志收集器
        self.case_logger = logging.getLogger(config("log", "logger_name"))

        # 2.指定日志收集器等级
        self.case_logger.setLevel(config("log", "logger_level"))

        # 原因：每次调用封装好的logger，程序都会添加一个handler，这就解释了，为什么会生成多少日志文件，因为每条myLog.logger().inf()都会写一个文件
        # 解决：在handler前面加个判断，如果logger已有handler，则不再添加handler
        if not self.case_logger.handlers:
            # 3.定义日志输出渠道
            # 输出到console控制台
            console_handle = logging.StreamHandler()

            # 输出到文件中
            file_handle = logging.FileHandler(LOGS_FILE_PATH, encoding='utf-8')

            # 4.指定日志输出渠道的日志等级
            console_handle.setLevel(config("log", "console_level"))
            file_handle.setLevel(config("log", "file_level"))

            # 5.定义日志显示的格式
            # 简单的日志格式
            simple_formatter = logging.Formatter(config("log", "simple_formatter"))
            # 复杂的日志格式
            verbose_formatter = logging.Formatter(config("log", "verbose_formatter"))

            console_handle.setFormatter(simple_formatter)    # 设置终端的日志为简单格式
            file_handle.setFormatter(verbose_formatter)    # 设置终端的日志为复杂模式

            # 6.对接，将日志收集器与输出渠道进行对接
            self.case_logger.addHandler(console_handle)
            self.case_logger.addHandler(file_handle)

    def get_logger(self):
        """
        获取日志器对象
        :return:
        """
        return self.case_logger

do_log = HandleLogging().get_logger()

if __name__ == '__main__':
    do_log = HandleLogging().get_logger()
    do_log.debug("这是debug日志")
    do_log.info("这是info日志")
    do_log.warning("这是warning日志")
    do_log.error("这是error日志")
    do_log.critical("这是critical日志")