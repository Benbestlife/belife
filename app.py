from flask import Flask
import secret
import config
from models.base_model import db

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.message import main as mail_routes, mail

from utils import format_time


def configured_app():
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    app.secret_key = secret.secret_key

    uri = 'mysql+pymysql://root:{}@localhost/belife?charset=utf8mb4'.format(
        secret.database_password
    )
    # 用于连接数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    # 如果设置成True(默认)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 初始化数据库
    db.init_app(app)

    # 自定义过滤器
    app.template_filter()(format_time)

    # flask-mail扩展发送电子邮件
    app.config['MAIL_SERVER'] = 'smtp.exmail.qq.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = config.admin_mail
    app.config['MAIL_PASSWORD'] = secret.mail_password
    mail.init_app(app)

    register_routes(app)
    return app


def register_routes(app):
    """
    蓝图（Blueprints）
    """
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(mail_routes, url_prefix='/mail')


if __name__ == '__main__':
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
        threaded=True,
    )
    app.run(**config)
