# -*- coding: utf-8 -*-
# @Project : iedge
# @Time    : 2021/3/22 10:33
# @Author  : Biao
# @FileName: __init__.py.py

import  os
from flask import  Flask
from flask_cors import CORS

from iedge.blueprints.api import api_bp

from iedge.settings import config
from iedge.extensions import db,login_manager
from iedge.models import User

def create_app(config_name=None):
	if config_name ==None:
		config_name = os.getenv("FLASK_CONFIG",'development')

	app = Flask('iedge')
	app.config.from_object(config[config_name])



	register_extensions(app)
	register_shell_context(app)
	register_blueprints(app)
	register_command(app)

	# register_fake()

	return app

def register_extensions(app):
	CORS(app, supports_credentials=True,resources=r'/*')

	db.init_app(app)
	#扩展初始化操作分离，自动创建表需要依赖程序上下文，两种方法
	#1.将app_context()通过push推送
	#2.创建上下文处理器，在flask run时，会自动执行；
	# with app.app_context():
	# 	# app.app_context().push()
	# 	db.create_all()
	login_manager.init_app(app)


def register_shell_context(app):
	@app.shell_context_processor
	def make_shell_context():
		# db.create_all()
		return dict(db=db,User=User)


def register_blueprints(app):
	app.register_blueprint(api_bp,url_prefix='/api')
#创建模拟数据

def register_command(app):
	@app.cli.command()
	def forge():
		from iedge.fakes import  faker_admin
		# db.drop_all()
		db.create_all()
		faker_admin()

	@app.cli.command()
	def init():
		print("initing the database ----")
		db.drop_all()





