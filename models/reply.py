import time

from sqlalchemy import Column, Integer, UnicodeText

from models.base_model import db, SQLMixin
from models.user import User


class Reply(SQLMixin, db.Model):
    content = Column(UnicodeText, nullable=False)
    topic_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def user(self):
        u = User.one(id=self.user_id)
        return u

    @classmethod
    def new(cls, form, user_id):
        from models.topic import Topic
        form['user_id'] = user_id
        m = super().new(form)
        topic = Topic.one(id=form['topic_id'])
        topic.reply_counts += 1
        return m

    def topic(self):
        # profile.html 中有用到
        # Topic 可能为 none, 在 profile 页面中做判断
        from models.topic import Topic
        t = Topic.one(id=self.topic_id)
        return t
