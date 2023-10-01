from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.database import get_db
from datetime import datetime
import io
from .validations.validate_blog import validate_blog_form

bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/')
@login_required
def index():
    user = g.user[0]

    posts = sharing_group_posts(user)

    user_groups = user_groups_func()
    return render_template('blog/index.html', posts=posts, current_url=request.path, user_groups = user_groups)

@bp.route('/favourites')
@login_required
def favourites():
    user = g.user[0]
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
    'SELECT DISTINCT p.id AS post_id, p.title, p.content, '
    'p.created, u.username AS post_owner,  f.user_id, u.id AS post_owner_id '
    'FROM posts p '
    'JOIN  favourite_posts_association f ON  p.id = f.post_id '
    'JOIN users u ON u.id = p.user_id '
    'WHERE f.user_id = %s ' 
    'ORDER BY p.created DESC',
    (user,)
)

    posts = cursor.fetchall()
    cursor.close()

    user_groups = user_groups_func()
    
    return render_template('blog/favourites.html', posts=posts, current_url=request.path, user_groups=user_groups)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        blog_form= {
            'title': request.form.get('title').strip(),
            'content': request.form.get('content').strip(),
            'created': datetime.utcnow()
        }

        error = None

        # Using validate_blog_form function to validate form data
        error = validate_blog_form(blog_form)

        if error is not None:
            flash(error, "danger")
        else:

            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO posts (title, content, created, user_id)'
                ' VALUES (%s, %s, %s, %s)',
                (blog_form['title'], blog_form['content'], blog_form['created'], g.user[0])
            )
            db.commit()
            cursor.close()

            return redirect(url_for('blog.index'))
    user_groups = user_groups_func()
    return render_template('blog/create.html', user_groups = user_groups)




@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        blog_form= {
            'title': request.form.get('title').strip(),
            'content': request.form.get('content').strip(),
            'created': datetime.utcnow()
        }
        error = None

        error = validate_blog_form(blog_form)


        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'UPDATE posts SET title = %s, content = %s'
                ' WHERE id = %s',
                (blog_form['title'], blog_form['content'], id)
            )
            db.commit()
            cursor.close()
            return redirect(url_for('blog.index'))
        
    user_groups = user_groups_func()

    return render_template('blog/update.html', post=post, user_groups = user_groups)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    if check_post_author(id):
        cursor = db.cursor()
        cursor.execute('DELETE FROM posts WHERE id = %s', (id,))
        db.commit() 
        cursor.close()
    return redirect(url_for('blog.index'))

@bp.route('/<int:id>/read', methods=('POST', 'GET'))
@login_required
def read(id):
    post = get_post(id)
    user = g.user[0]
    if request.method == 'POST':
        is_favourite = request.form.get('not_favourite') or request.form.get('favourite')
        db = get_db()
        cursor = db.cursor()

        if is_favourite == 'True':
            cursor.execute(
                'INSERT INTO favourite_posts_association (user_id, post_id) VALUES (%s, %s)',
                (user, id)
            )
        else:
            cursor.execute(
                'DELETE FROM favourite_posts_association WHERE user_id = %s AND post_id = %s',
                (user, id)
            )

        db.commit()
        cursor.close()

        # Redirect to the 'favourites' route after handling the favorite action
        return redirect(url_for('blog.favourites'))

    if post is None:
        # Handle the case where the post with the given ID is not found
        return "Post not found", 404
    
    is_favourite = favourite_post_of_user(user, id)

    
    # Render the 'read.html' template for GET requests
    user_groups = user_groups_func()
    return render_template('blog/read.html', post=post, is_favourite =  is_favourite, user_groups = user_groups)


def get_post(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT p.id, title, content, created, user_id, username'
        ' FROM posts p JOIN users u ON p.user_id = u.id'
        ' WHERE p.id = %s',
        (id,)
    )
    post = cursor.fetchone()
    cursor.close()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post

def check_post_author(id):
    post = get_post(id)

    if  post[4] != g.user[0]:
        abort(403)
    else:
        return True

def favourite_post_of_user(user_id, post_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT 1 '
        ' FROM  favourite_posts_association f '
        ' WHERE f.user_id = %s AND f.post_id = %s',
        (user_id, post_id)
    )
    result = cursor.fetchone()
    cursor.close()
    return result

def sharing_group_posts(user):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT DISTINCT p.id, p.title, p.content, p.created, u.username, p.user_id '
        'FROM posts p '
        'JOIN users u ON p.user_id = u.id '
        'JOIN user_group_association ua1 ON u.id = ua1.user_id '
        'JOIN user_group_association ua2 ON ua1.group_id = ua2.group_id '
        'WHERE ua2.user_id = %s',
        (user,)
    )

    results = cursor.fetchall()
    cursor.close()

    return results

def user_groups_func():
    user_id = g.user[0] if g.user else None
    if user_id is None:
        return []  # Return an empty list if the user is not logged in

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT DISTINCT g.name FROM user_group_association as us_gr '
        'JOIN groups as g ON us_gr.group_id = g.id '
        'WHERE us_gr.user_id = %s',
        (user_id,)
    )
    results = cursor.fetchall()
    cursor.close() 

    return results

