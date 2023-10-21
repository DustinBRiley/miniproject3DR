from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from games.auth import login_required
from games.db import get_db

bp = Blueprint('games', __name__)

@bp.route('/')
def index():
    db = get_db()
    games = db.execute(
        'SELECT g.title, console'
        ' FROM games g JOIN user u ON g.player_id = u.id'
        ' ORDER BY g.title DESC'
    ).fetchall()
    return render_template('games/index.html', games=games)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        console = request.form['console']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO games (title, console, player_id)'
                ' VALUES (?, ?, ?)',
                (title, console, g.user['id'])
            )
            db.commit()
            return redirect(url_for('games.index'))

    return render_template('games/create.html')