# import redis
# import json
from flask import (
    render_template,
    # redirect,
    # url_for,
    Blueprint,
)

from routes import *

from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)
# cache = redis.StrictRedis()


@main.route("/")
@login_required
def index():
    u = current_user()
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    token = new_csrf_token()
    bs = Board.all()
    return render_template("topic/index.html", ms=ms, token=token, bs=bs, bid=board_id, user=u)


# def cache_topic(topic_id):
#     k = 'cache_topic_{}'.format(topic_id)
#     if cache.exists(k):
#         v = cache.get(k)
#         topic = json.loads(v)
#         print('测试', type(topic), topic)
#         return topic
#     else:
#         topic = Topic.get(topic_id)
#         v = json.dumps(topic.json())
#         cache.set(k, v)
#         return topic


@main.route('/<int:id>')
def detail(id):
    u = current_user()
    m = Topic.get(id)
    board = Board.one(id=m.board_id)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, user=u, board=board)


@main.route("/delete")
@csrf_required
def delete():
    id = int(request.args.get('id'))
    Topic.delete(id)
    return redirect(url_for('.index'))


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    Topic.new(form, user_id=u.id)
    return redirect(url_for('.index'))
