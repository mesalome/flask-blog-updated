import re
def validate_auth_form(form: dict) -> str:
        username = form.get('username')
        first_name = form.get('first_name')
        last_name = form.get('last_name')
        email = form.get('email')
        password = form.get('password')

        spaces_in_username = re.search(' ', username)
        spaces_in_password = re.search(' ', password)
        
        def strong_password(text):
            return re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%^&*()_\-+={[}\]|:;\"'<,>.?/]).{8,}$", text)

        if not username:
            return 'Username is required.'
        elif spaces_in_username:
            return "Username can't contain spaces."
        elif not first_name:
            return 'First Name is required.'
        elif not last_name:
            return 'First Name is required.'
        elif not email:
            return 'Email is required.'
        elif not password:
            return 'Password is required.'
        elif spaces_in_password:
            return "Password can't contain spaces."
        elif len(password) < 8:
            return "Password must contain at least 8 characters."
        elif not strong_password(password):
            return "Password must contain upper and lower case letters, numbers, and special characters."