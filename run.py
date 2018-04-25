# -*- coding: UTF-8 -*-
# __author__ = 'leyex@seeapp.com'
# __file_name__ = 'run'

from app import app
from config.config import RunConfig


if __name__ == '__main__':
    app.run(host=RunConfig.HOST, port=RunConfig.PORT, debug=RunConfig.DEBUG, threaded=RunConfig.THREADED)
