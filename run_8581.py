# -*- coding: UTF-8 -*-
# __author__ = 'leyex@seeapp.com'
# __file_name__ = 'run_8581'

from app import app
from config.config import RunConfigTester as RunConfig


if __name__ == '__main__':
    app.run(host=RunConfig.HOST, port=RunConfig.PORT, debug=RunConfig.DEBUG, threaded=RunConfig.THREADED)
