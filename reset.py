from sqlalchemy import create_engine

import secret
from app import configured_app
from models.base_model import db
from models.board import Board
from models.reply import Reply
from models.topic import Topic
from models.user import User


def reset_database():
    # 此时 mysql root 默认用 socket 来验证而不是密码
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(
        secret.database_password
    )
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS belife')
        c.execute('CREATE DATABASE belife CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE belife')
    db.metadata.create_all(bind=e)


def generate_fake_date():
    form = dict(
        username='abc',
        password='123',
    )
    User.register(form)

    form = dict(
        username='test',
        password='123456',
    )
    u = User.register(form)

    form = dict(
        title='全部',
    )
    b = Board.new(form)
    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    topic_form = dict(
        title='markdown demo',
        board_id=b.id,
        content=content
    )

    for i in range(2):
        print('begin topic <{}>'.format(i))
        t = Topic.new(topic_form, u.id)

        reply_form = dict(
            content='reply test',
            topic_id=t.id,
        )
        for j in range(2):
            Reply.new(reply_form, u.id)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
