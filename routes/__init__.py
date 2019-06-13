import uuid
import redis
import json

from functools import wraps
from flask import (
    session,
    request,
    abort,
    redirect,
    url_for,
)

from models.user import User


cache = redis.StrictRedis()


def current_user():
    uid = session.get('user_id', '')
    u = User.one(id=uid)
    return u


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        u = current_user()
        if u is None:
            return redirect(url_for('index.index'))
        else:
            return f(*args, **kwargs)
    return wrapper


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        k = 'csrf_tokens_{}'.format(token)
        v = cache.get(k)
        ks = json.loads(v)
        if cache.exists(k) and ks == u.id:
            cache.delete(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    k = 'csrf_tokens_{}'.format(token)
    v = json.dumps(u.id)
    cache.set(k, v)
    return token


def topic_time_sorted(ilist):
    for i in range(len(ilist)):
        for j in range(i):
            if ilist[i]['created_time'] > ilist[j]['created_time']:
                ilist.insert(j, ilist.pop(i))
                break
    return ilist


def reply_time_sorted(ilist):
    for i in range(len(ilist)):
        for j in range(i):
            if ilist[i].created_time > ilist[j].created_time:
                ilist.insert(j, ilist.pop(i))
                break
    return ilist
