# -*- coding: utf-8 -*-
# @Project : iedge
# @Time    : 2021/3/22 16:43
# @Author  : Biao
# @FileName: utils.py
import jwt,datetime

def generate_jwt(payload, expiry, secret=None):
	_payload = {'exp': expiry}
	_payload.update(payload)

	if not secret:
		secret = "secret"

	token = jwt.encode(_payload, secret, algorithm='HS256')
	# print(type(token))
	return token


def verify_jwt(token, secret=None):
	if not secret:
		secret = "secret"
	try:
		payload = jwt.decode(token, secret, algorithms=['HS256'])
	# print("payload is {}".format(payload))
	except jwt.PyJWTError:
		payload = None

	return payload

def generate_tokens(user_id,refresh=True):
	
	now = datetime.datetime.utcnow()
	expiry = now + datetime.timedelta(hours=0.5)
	token = generate_jwt({"user_id":user_id},expiry)
	refresh_token= None
	if refresh:
		refresh_expiry = now+datetime.timedelta(days=14)
		refresh_token = generate_jwt({"user_id":user_id,"is_refresh":True},refresh_expiry)
	return token,refresh_token
		