from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.board import Board


main = Blueprint('board', __name__)


@main.route("/admin")
@login_required
def index():
    bs = Board.all()
    return render_template('board/admin_index.html', bs=bs)


@main.route("/add", methods=["POST"])
@login_required
def add():
    form = request.form
    Board.new(form)
    return redirect(url_for('topic.index'))

