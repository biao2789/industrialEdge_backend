# -*- coding: utf-8 -*-
# @Project : iedge
# @Time    : 2021/3/22 16:36
# @Author  : Biao
# @FileName: api.py

import datetime,urllib.parse
from flask import Blueprint,jsonify,request,g,make_response
from iedge.fakes import  fake_table_data
from  iedge.utils import  generate_jwt,verify_jwt,generate_tokens
from iedge.models import User
from iedge.extensions import db

# from flask_login import  current_user,login_fresh,login_user


api_bp = Blueprint('api',__name__)


@api_bp.before_request
def before_request():
    g.user_id=None
    g.is_refresh = False
    
    if '/login' in request.path:
        return None
    else:
        # Vue针对复杂请求会产生“OPTIONS预检请求，
        if request.method == 'OPTIONS':
            return jsonify(code=20000),203
        token = request.headers.get('Authorization')
            # print("token is {}".format(token))
        if token is not None and token.startswith('Bearer '):
            token = token[7:]
            
            # 验证token
            payload = verify_jwt(token)
            # print("payload is {}".format(payload))
            
            if payload is not None:
                # 保存到g对象中
                g.user_id = payload.get('user_id')
                g.is_refresh = payload.get('is_refresh', False)

@api_bp.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin","*")
    response.headers.add("Access-Control-Allow-Methods",'GET,POST,OPTIONS')
    response.headers.add("Access-Control-Allow-Headers","*")
    return response


@api_bp.route("/vue-admin-template/table/list",methods=["GET"])
def loadData():

    user = User.query.filter_by(id=g.user_id).first_or_404()
    if user is not None:
        res = fake_table_data()
        return jsonify(res)



@api_bp.route('/vue-admin-template/user/login', methods=['POST'])
def user_login():
    # if current_user.is_authenticated:
    #     return jsonify(dict(code=20000))
    # print("login")

    username = request.json.get("username")
    password = request.json.get("password")
    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        token,refresh_token =generate_tokens(user.id)
        return jsonify(dict(code=20000, data={"token": token}))
    return jsonify(dict(code =40001, message="登录失败")),401


@api_bp.route('/vue-admin-template/user/info', methods=['GET'])
def user_info():
    user = User.query.filter_by(id=g.user_id).first()
    if user is not None :
        info = dict(avatar='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                    name=user.username)
        return jsonify(dict(code=20000, data=info))
    return jsonify(dict(code=20001, data="error"))


@api_bp.route("/vue-admin-template/user/reset-password",methods=['POST','OPTIONS'])
def reset_password():
    if request.method=="OPTIONS":
        return jsonify(code=200),203
    password = request.json.get("password")
    new_password = request.json.get("new_password")
    user = User.query.filter_by(id=g.user_id).first()

    if user is not None and user.verify_password(password):
        user.set_password(new_password)
        db.session.commit()
        return jsonify(dict(code=20000, data="password modify success!"))
    return jsonify(dict(code=20001,message="Update Failed!")),403
    

@api_bp.route('/vue-admin-template/user/logout', methods=['POST'])
def user_logout():
	return jsonify({"code": 20000, "data": 'success'})