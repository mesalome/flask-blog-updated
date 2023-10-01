from flask import Blueprint, make_response, jsonify, request
from ..models import Post, User, Group
from ..database import get_db
from ..token.jwt_token import decode_auth_token

blog_blueprint = Blueprint("blogAPI", __name__, url_prefix="/api/blog")

@blog_blueprint.route("/", methods=["GET"])
def index():
    # Checking if the user is authenticated
    if not is_authenticated(request):
        response = {
            "status": "fail",
            "message": f"User is not authenticated."
        }
        return make_response(jsonify(response)), 401

    user = get_authenticated_user(request)
    if user is None:
        response = {
            "status": "fail",
            "message": "User not found."
        }
        return make_response(jsonify(response)), 404

    # Getting user's groups
    user_groups = get_user_groups(user)

    # Gettting posts whose authors intersect with the user's groups
    posts = get_posts_in_user_groups(user_groups)

    response = {
        "status": "success",
        "message": "Posts retrieved successfully.",
        "posts": posts
    }

    return make_response(jsonify(response ))

@blog_blueprint.route("/<int:id>/update", methods=["GET", "POST"])
def update(id):

    post = get_post(id)

    # Making sure post exists
    if post is None:
        response = {
            "status": "fail",
            "message": "Post not found."
        }
        return make_response(jsonify(response)), 404
    
    # Checking if the user is authenticated
    if not is_authenticated(request):
        response = {
            "status": "fail",
            "message": f"User is not authenticated."
        }
        return make_response(jsonify(response)), 401

    user = get_authenticated_user(request)
    if user is None:
        response = {
            "status": "fail",
            "message": "User not found."
        }
        return make_response(jsonify(response)), 404
    
    #Checking if user is the author of the blog
    if user != get_post_author_username(id):
        response = {
            "status": "fail",
            "message": "You are not authorized to update this post.",
        }
        return make_response(jsonify(response)), 403
    
    #Post method
    if request.method == 'POST':
        post_data = request.get_json()
        if not validate_blog_data(post_data['title'], post_data['content']):
            response = {
            "status": "Fail",
            "message": "Title or Content length is not acceptable.",
            "posts": post_data
            }
            return make_response(jsonify(response)), 500
        else: 
            response = {
                "status": "success",
                "message": "Posts updated successfully.",
                "posts": post_data
            }

            return make_response(jsonify(response )), 200
    
    #GET method
    else:
        response = {
            "status": "success",
            "message": "POST method for updating is successfully rendered.",
            "posts": post
        }
        
        return make_response(jsonify(response )), 200
    

@blog_blueprint.route("/<int:id>/delete", methods=["POST"])
def delete(id):

    post = get_post(id)

    # Making sure post exists
    if post is None:
        response = {
            "status": "fail",
            "message": "Post not found."
        } 
        return make_response(jsonify(response)), 404
    
    # Checking if the user is authenticated
    if not is_authenticated(request):
        response = {
            "status": "fail",
            "message": f"User is not authenticated."
        }
        return make_response(jsonify(response)), 401

    user = get_authenticated_user(request)
    if user is None:
        response = {
            "status": "fail",
            "message": "User not found."
        }
        return make_response(jsonify(response)), 404
    
    #Checking if user is the author of the blog
    if user != get_post_author_username(id):
        response = {
            "status": "fail",
            "message": "You are not authorized to delete this post.",
        }
        return make_response(jsonify(response)), 403
    
    #Post method
    if request.method == 'POST':
        response = {
            "status": "success",
            "message": "Posts has been deleted successfully.",
            "posts": post
        }

        return make_response(jsonify(response )), 200
    
@blog_blueprint.route("/create", methods=["GET", "POST"])
def create():
    
    # Checking if the user is authenticated
    if not is_authenticated(request):
        response = {
            "status": "fail",
            "message": f"User is not authenticated."
        }
        return make_response(jsonify(response)), 401

    user = get_authenticated_user(request)
    if user is None:
        response = {
            "status": "fail",
            "message": "User not found."
        }
        return make_response(jsonify(response)), 404
    
    post_data = request.get_json()

    title = post_data['title']
    content = post_data['content']

    if not validate_blog_data(title, content):
        response = {
            "status": "Fail",
            "message": "Title or Content length is not acceptable.",
            "posts": post_data
        }
        return make_response(jsonify(response)), 500
    #Post method
    if request.method == 'POST':

        response = {
            "status": "success",
            "message": "Posts created successfully.",
            "posts": post_data
        }

        return make_response(jsonify(response )), 200
    
    #GET method
    else:
        response = {
            "status": "success",
            "message": "Post method for creating is successfully rendered.",
        }
        return make_response(jsonify(response )), 200
def is_authenticated(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return False

    try:
        _, token = auth_header.split(" ")
        _, error = decode_auth_token(token)
        if error is not None:
            return False
        return True
    except ValueError:
        return False


def get_authenticated_user(request):
        if is_valid_token(request):
            return get_user_id_from_token(request)
        return None
        
def get_user_groups(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT g.name FROM groups g "
        "JOIN user_group_association us_gr ON g.id = us_gr.group_id "
        "JOIN users u ON us_gr.user_id = u.id "
        "WHERE u.username = %s",
        (username,)
    )
    groups = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return groups

def get_posts_in_user_groups(user_groups):
    db = get_db()
    cursor = db.cursor()
    posts = []
    for user_group_name in user_groups:
        cursor.execute('''SELECT * FROM posts 
                       WHERE posts.user_id 
                       IN (SELECT users.id FROM users 
                       JOIN user_group_association usgr 
                       ON users.id = usgr.user_id JOIN groups 
                       ON usgr.group_id = groups.id 
                       WHERE groups.name = %s);''',
        (user_group_name,)
        )
    posts.extend(cursor.fetchall()) 
    cursor.close()
    return posts

def is_valid_token(request):
    auth_header = request.headers.get("Authorization")
    _, token = auth_header.split(" ")
    user, error = decode_auth_token(token)
    return not error

    
def get_user_id_from_token(request):
    auth_header = request.headers.get("Authorization")
    _, token = auth_header.split(" ")
    user, error = decode_auth_token(token)
    if not error:
        return user
    else:
        return None

def get_post(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM posts WHERE posts.id = %s ''',
                   (id,))
    post = cursor.fetchone()
    cursor.close()
    return post

def get_post_author_username(post_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''SELECT users.username FROM users 
                   JOIN posts ON users.id = posts.user_id 
                   WHERE posts.id = %s ''',
                   (post_id,))
    username = cursor.fetchone()[0]
    cursor.close()

    return username 

def validate_blog_data(title, content):
    title = title.strip()
    content = content.strip()
    if len(title) > 0 or len(title) <= 100:
        return True
    elif len(content) >= 80 or len(content) <= 1000:
        return True
    else:
        return False