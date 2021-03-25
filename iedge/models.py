# -*- coding: utf-8 -*-
# @Project : iedge
# @Time    : 2021/3/22 11:21
# @Author  : Biao
# @FileName: models.py

from  iedge.extensions import db
from flask_login import UserMixin
from werkzeug.security import  generate_password_hash ,check_password_hash

class User(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String,unique= True)

	password_hash = db.Column(db.String(128))


	def set_password(self,password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)





