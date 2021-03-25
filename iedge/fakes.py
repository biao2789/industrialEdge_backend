# -*- coding: utf-8 -*-
# @Project : iedge
# @Time    : 2021/3/22 13:35
# @Author  : Biao
# @FileName: fakes.py


from faker import Faker
from iedge.models import  User
from iedge.extensions import  db

fake = Faker()

def faker_admin():

    admin = User.query.filter_by(username="admin").first()
    if  not admin:
        admin = User(username='admin')
        admin.set_password('111111')
        db.session.add(admin)
        db.session.commit()

def fake_table_data(count=20):
    res = dict(code=20000)
    items = []
    for i in range(count):
        item = dict(id=fake.random_digit(),
                    title=fake.word(),
                    author=fake.name(),
                    display_time=fake.date_time().strftime("%Y-%m-%dT%H:%M:%S"),
                    pageviews=100)
        # print(type(fake.date_time()))
        # print(fake.date_time().strftime("%Y-%m-%dT%H:%M:%S"))
        items.append(item)
    res["data"] = dict(total=len(items), items=items)
    return res
