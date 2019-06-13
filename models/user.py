import hashlib

from sqlalchemy import Column, String

import config
from models.base_model import SQLMixin, db


class User(SQLMixin, db.Model):
    __tablename__ = 'User'

    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False, default='/images/3.jpg')
    email = Column(String(50), nullable=False, default=config.test_mail)
    signature = Column(String(100), nullable=False, default='什么也没有留下')

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        if len(name) > 3 and User.one(username=name) is None:
            form['password'] = User.salted_password(form['password'])
            u = User.new(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        return User.one(**query)
