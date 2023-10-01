from flask import Blueprint, render_template,request

from .blog import user_groups_func

bp = Blueprint('about', __name__, url_prefix='/about')

@bp.route('/')
def index():
    user_groups = user_groups_func()
    return render_template('about.html', current_url=request.path, user_groups = user_groups)
