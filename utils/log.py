# -*- coding: UTF-8 -*-
# __author__ = 'leyex@seeapp.com'
# __file_name__ = 'log'

import re
import os
import random
import logging
import logging.handlers


def out_log(dirpath='./log', log_name='WechatSite', logtofile=True):  # 日志输出
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    filename = os.path.join(dirpath, log_name)

    fmt = logging.Formatter('%(asctime)s - %(name)-12s:%(funcName)s - [%(levelname)-8s] - %(message)s')
    log = logging.getLogger(str(random.random()))

    # 标准输出
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(fmt)
    if not log.handlers:
        log.addHandler(console)

        # 文件输出
        if logtofile:

            rotating = logging.handlers.TimedRotatingFileHandler(filename=filename, when="midnight", interval=1,
                                                                 backupCount=7)
            rotating.suffix = "%Y-%m-%d.log"
            rotating.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
            rotating.setFormatter(fmt)
            log.addHandler(rotating)

    log.setLevel(logging.DEBUG)
    return log
