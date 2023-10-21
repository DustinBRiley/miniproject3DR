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
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('games/index.html', games=games)