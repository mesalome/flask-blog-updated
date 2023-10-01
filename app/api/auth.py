from flask import Blueprint, make_response, jsonify, request
from app.auth_token import BlackJWToken
from app.token.jwt_token import encode_auth_token, decode_auth_token
from ..validations.validate_auth import validate_auth_form
from werkzeug.security import check_password_hash
from app.database import get_db 

auth_blueprint = Blueprint('authAPI', __name__, url_prefix='/api/auth')

@auth_blueprint.route('/register', methods=['POST'])
def register():
    post_data = request.get_json()

    # Checks if user submits valid data during registration
    if error := validate_auth_form(post_data):
        response = {
            "status": "fail",
            "message": error
        }
        return make_response(jsonify(response)), 400

    username = post_data['username']  
    
    # Checks if the user with the given username already exists
    if is_user_already_registered(username):
        response = {
            "status": "fail",
            "message": f"User {username} is already registered."
        }
        return make_response(jsonify(response)), 409  
    
    email = post_data['email']  
    
    # Checks if the user with the given email already exists
    username = post_data['email']  
    if is_user_already_registered(username):
        response = {
            "status": "fail",
            "message": f"{email} has already been used."
        }
        return make_response(jsonify(response)), 409  
    
    

    #Successful registration - Data is valid, username and email don't exist
    response = {
        "status": "Success",
        "message": "Successfully Registered. Please Log in!"
    }
    
    return make_response(jsonify(response)), 201  



@auth_blueprint.route('/login', methods=['POST'])
def login():
    post_data = request.get_json()

    username = post_data['username']
    input_password = post_data['password']

    # Checks if submitted data is valid 
    if error := validate_auth_form(post_data):
        response = {
            "status": "fail",
            "message": error
        }
        return make_response(jsonify(response)), 400
    
    # Checks if given username exists
    if not is_user_already_registered(username):
        response = {
            "status": "fail",
            "message": "Invalid username or password."
        }
        return make_response(jsonify(response)), 401 

    # Check if the provided password is correct
    if not is_password(username, input_password):
        response = {
            "status": "fail",
            "message": "Invalid username or password."
        }
        return make_response(jsonify(response)), 401 

    # Successful login
    auth_token = encode_auth_token(username)

    response = {
        "status": "Success",
        "message": "Login successful.",
        "auth_token": auth_token  # Include the auth token in the response
    }

    return make_response(jsonify(response)), 200



@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        response = {
            "status": "Fail",
            "message": "Authorization header not provided!"
        }
        return make_response(jsonify(response)), 400
    
    _, token = auth_header.split(" ")
    _, error = decode_auth_token(token)

    if error:
        response = {
            "status": "Fail",
            "message": error
        }
        return make_response(jsonify(response)), 400
    
    BlackJWToken(token).commit()

    response = {
            "status": "Success",
            "message": "Successfully logged out"
        }
    
    return make_response(jsonify(response)), 200




def is_user_already_registered(username):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        return cursor.fetchone() is not None

def is_email_already_used(email):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
        return cursor.fetchone() is not None
    

def is_password(username, input_password):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        stored_password = cursor.fetchone()
        if stored_password:
            return check_password_hash(stored_password[0], input_password)
        return False
