import os
import uuid
import json
import redis

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    send_from_directory,
)
from werkzeug.datastructures import FileStorage
# from werkzeug.utils import secure_filename

from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import (
    current_user,
    topic_time_sorted,
    reply_time_sorted,
    new_csrf_token,
    csrf_required,
    login_required,
)

cache = redis.StrictRedis()
main = Blueprint('index', __name__)


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    User.register(form)
    return redirect(url_for('.index'))


@main.route("/register/view")
def register_view():
    return render_template("user/register.html")


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route("/logout")
def logout():
    session.pop('user_id')
    return redirect(url_for('index.index'))


def created_topic(user_id):
    k = 'created_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        return ts
    else:
        ts = Topic.all(user_id=user_id)
        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)
        return ts


def replied_topic(user_id):
    k = 'replied_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        return ts
    else:
        rs = Reply.all(user_id=user_id)
        ts = []
        for r in rs:
            t = Topic.one(id=r.topic_id)
            ts.append(t)

        v = json.dumps([t.json() for t in ts if t is not None])
        cache.set(k, v)

        return ts


@main.route('/profile')
@login_required
def profile():
    u = current_user()
    return render_template(
        'user/profile.html',
        user=u,
    )


@main.route('/user/<int:id>')
@login_required
def user_detail(id):
    # TODO 需要修改
    u = User.one(id=id)
    topics = created_topic(u.id)
    topics = topic_time_sorted(topics)
    print('测试', topics)
    # topics = Topic.all(user_id=u.id)
    # topics = time_sorted(topics)
    reply = Reply.all(user_id=u.id)
    reply = reply_time_sorted(reply)
    return render_template('user/profile.html', user=u, topics=topics, reply=reply)


@main.route('/setting')
@login_required
def setting():
    token = new_csrf_token()
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    else:
        return render_template(
            'user/setting.html',
            user=u,
            token=token,
        )


@main.route('/info/update', methods=['POST'])
@csrf_required
def info_update():
    form = request.form.to_dict()
    u = current_user()
    User.update(u.id, **form)
    return redirect(url_for('index.setting'))


@main.route('/password/update', methods=['POST'])
@csrf_required
def password_update():
    form = request.form.to_dict()
    old_pass = form['old_pass']
    new_pass = User.salted_password(form['new_pass'])
    u = current_user()
    query = dict(
        username=u.username,
        password=old_pass,
    )
    if bool(User.validate_login(query)) is True:
        User.update(u.id, password=new_pass)
        return redirect(url_for('index.setting'))
    else:
        return redirect(url_for('index.index'))


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file: FileStorage = request.files['avatar']
    # file = request.files['avatar']
    # filename = file.filename
    # ../../root/.ssh/authorized_keys
    # images/../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))
    return redirect(url_for('index.setting'))


@main.route('/images/<filename>')
def image(filename):
    # 直接拼接路由不安全，比如
    # http://localhost:2000/images/..%5Capp.py
    # path = os.path.join('images', filename)
    # print('images path', path)
    # return open(path, 'rb').read()
    # if filename in os.listdir('images'):
    #     return
    return send_from_directory('images', filename)
