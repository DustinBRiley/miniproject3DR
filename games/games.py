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
        'SELECT ga.id, title, console, player_id'
        ' FROM games ga JOIN user u ON ga.player_id = u.id'
        ' ORDER BY ga.title DESC'
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

def get_game(id):
    game = get_db().execute(
        'SELECT ga.id, player_id, title, console'
        ' FROM games ga JOIN user u ON ga.player_id = u.id'
        ' WHERE ga.id = ?',
        (id,)
    ).fetchone()

    if game is None:
        abort(404, f"Game id {id} doesn't exist.")

    if game['player_id'] != g.user['id']:
        abort(403)

    return game

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    game = get_game(id)

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
                'UPDATE games SET title = ?, console = ?'
                ' WHERE id = ?',
                (title, console, id)
            )
            db.commit()
            return redirect(url_for('games.index'))

    return render_template('games/update.html', game=game)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_game(id)

    db = get_db()
    db.execute('DELETE FROM games WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('games.index'))