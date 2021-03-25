# -*- coding: utf-8 -*-
# @Project : iedge
# @Time    : 2021/3/22 10:39
# @Author  : Biao
# @FileName: settings.py.py
import  os,sys

basedir= os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class BaseConfig():
	SQLALCHEMY_TRACK_MODIFICATIONS= False
	pass

class DevelopmentConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'iedge_dev.sqlite')
	# SQLALCHEMY_DATABASE_URI="sqlite:///F:/opensource/iedge/iedge_dev.sqlite"
	SQLALCHEMY_TRACK_MODIFICATIONS = False




class ProductionConfig(BaseConfig):
	pass

config = {"development": DevelopmentConfig,
          "production":ProductionConfig}