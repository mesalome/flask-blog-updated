from flask import (
    Blueprint, render_template
)
from .blog import user_groups_func

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    user_groups = user_groups_func()
    return render_template('index.html', user_groups = user_groups)