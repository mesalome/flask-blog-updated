import functools
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
from app.database import get_db
from .validations.validate_auth import validate_auth_form
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        post_data = {
            'username': request.form.get('username').lower(),
            'first_name': request.form.get('first_name').strip().lower(),
            'last_name': request.form.get('last_name').strip().lower(),
            'email': request.form.get('email').strip().lower(),
            'password': request.form.get('password'),
        }

        # Using validate_auth_form function to validate form data
        error = validate_auth_form(post_data)

        if error is None:
            db = get_db()
            try:
                with db.cursor() as cursor:
                    # Check if the username is already registered
                    cursor.execute(
                        "SELECT id FROM users WHERE username = %s",
                        (post_data['username'],)
                    )
                    existing_username = cursor.fetchone()
                    
                    # Check if the email has already been used
                    cursor.execute(
                        "SELECT id FROM users WHERE email = %s",
                        (post_data['email'],)
                    )
                    existing_email = cursor.fetchone()

                    if existing_username:
                        error = f"Username {post_data['username'].capitalize()} is already registered."
                    elif existing_email:
                        error = f"Email {post_data['email']} has already been used."
                    else:
                        cursor.execute(
                            "INSERT INTO users (username, first_name, last_name, email, password) VALUES (%s, %s, %s, %s, %s)",
                            (post_data['username'], post_data['first_name'], post_data['last_name'], post_data['email'], generate_password_hash(post_data['password'])),
                        )
                        
                        db.commit()
                        
                        cursor.execute("SELECT * FROM groups")
                        available_groups = cursor.fetchall()
                        cursor.execute("SELECT id FROM users WHERE username = %s", (post_data['username'],))
                        user_id = cursor.fetchone()
                        for group in available_groups:
                            group_id = group[0]
                            field_name = f"group_{group_id}"
                            if field_name in request.form and request.form[field_name] == "on":
                                cursor.execute(
                                    "INSERT INTO user_group_association (user_id, group_id) VALUES (%s, %s)",
                                    (user_id, group_id)
                                )
                        
                        db.commit()

                        return redirect(url_for("auth.login"))
            except Exception as e:
                error = str(e)
                db.rollback() 

        flash(error, "danger")

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM groups")
        groups = cursor.fetchall()

    return render_template('auth/register.html', groups=groups)




@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            cursor = db.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE username = %s',
                (username,)
            )
            user = cursor.fetchone()
            cursor.close()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user[5], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user[0]
                return redirect(url_for('blog.index'))

        flash(error, "danger")

    return render_template('auth/login.html')



@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cursor = get_db().cursor()
        cursor.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        user = cursor.fetchone()
        cursor.close()

        if user is None:
            g.user = None
        else:
            g.user = user


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

