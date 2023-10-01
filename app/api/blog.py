from flask import Blueprint

blog_blueprint = Blueprint("blogAPI", __name__, url_prefix="/api/blog")