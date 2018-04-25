# -*- coding: UTF-8 -*-
# __author__ = 'leyex@seeapp.com'
# __file_name__ = '__init__.py'

from flask import Flask
from app.siciyuan import views
from utils.log import out_log as logger

app = Flask(__name__)   # 实例化flask对象



