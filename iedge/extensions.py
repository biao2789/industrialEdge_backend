# -*- coding: utf-8 -*-
# @Project : iedge
# @Time    : 2021/3/22 10:58
# @Author  : Biao
# @FileName: extensions.py


from flask_sqlalchemy import  SQLAlchemy
from flask_login import LoginManager,AnonymousUserMixin

db= SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from iedge.models import User
    user = User.query.get(int(user_id))
    print("user")
    print(user)
    return user


login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'auth.re_authenticate'
# login_manager.needs_refresh_message = 'Your custom message'
login_manager.needs_refresh_message_category = 'warning'


class Guest(AnonymousUserMixin):

    def can(self, permission_name):
        return False

    @property
    def is_admin(self):
        return False




