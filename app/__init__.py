# -*- coding: UTF-8 -*-
# __author__ = 'leyex@seeapp.com'
# __file_name__ = '__init__.py'

from flask import Flask

app = Flask(__name__)   # 实例化flask对象

<<<<<<< HEAD

from app.siciyuan import views
=======
from app.siciyuan import views
from utils.log import out_log as logger
>>>>>>> 754dde9400cb3571a9462230db08b22095ae337e

