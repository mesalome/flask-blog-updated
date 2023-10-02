import requests

import json

import time

def test_register_with_valid_data():
    data = {
        'username': 'test_user_3',
        'email': 'test@test2.com',
        'first_name': 'test',
        'last_name': 'user 2',
        'password': 'Test123!!',
    }

    resp = requests.post(
        url='http://127.0.0.1:5000/api/auth/register',
        json=data
    )
    
    try:
        response_data = resp.json()
        print(response_data)
    except json.JSONDecodeError:
        print("Failed to parse response as JSON. Response content:", resp.text)

def test_register_with_data_already_in_database():
    data = {
        'username': 'test_user_1',
        'email': 'test@test.com',
        'first_name': 'test',
        'last_name': 'user',
        'password': 'Test123!',
    }

    resp = requests.post(
        url='http://127.0.0.1:5000/api/auth/register',
        json=data
    )
    
    try:
        response_data = resp.json()
        print(response_data)
    except json.JSONDecodeError:
        print("Failed to parse response as JSON. Response content:", resp.text)

def test_register_with_invalid_password_with_spaces():
    data = {
        'username': 'test_user',
        'email': 'test@test.com',
        'first_name': 'test',
        'last_name': 'user',
        'password': '  ',  #no password
    }

    resp = requests.post(
        url='http://127.0.0.1:5000/api/auth/register',
        json=data
    )
    print(resp.json())

def test_register_with_inavlid_password():
    data = {
        'username': 'test_user',
        'email': 'test@test.com',
        'first_name': 'test',
        'last_name': 'user',
        'password': 'password',   #no capital letters, numbers or special characters
    }

    resp = requests.post(
        url='http://127.0.0.1:5000/api/auth/register',
        json=data
    )
    print(resp.json())


def test_login_with_valid_data():
    login_data = {
        'username': 'test_user_1',
        'email': 'test@test.com',
        'first_name': 'test',
        'last_name': 'user',
        'password': 'Test123!',
    }

    resp = requests.post(
        url='http://127.0.0.1:5000/api/auth/login',
        json=login_data  
    )

    if resp.status_code == 200:
        # Parse JSON content only if the response contains JSON data
        json_data = resp.json()
        print(json_data)
        # Add your assertions and further testing logic here
    else:
        # Handle non-200 status codes if needed
        print(f"Request failed with status code {resp.status_code}: {resp.text}")

def test_login_with_invalid_data():
    login_data = {
        'username': 'test_user_1',
        'email': 'test@test.com',
        'first_name': 'test',
        'last_name': 'user',
        'password': 'Test123!!!!!!', #Invalid Password
    }

    resp = requests.post(
        url='http://127.0.0.1:5000/api/auth/login',
        json=login_data 
    )

    
    print(resp.json())

def test_logout_with_valid_data():
    data = {
        'username': 'test_user_1',
        'email': 'test@test.com',
        'first_name': 'test',
        'last_name': 'user',
        'password': 'Test123!',
    }


    resp = requests.post(
        url='http://127.0.0.1:5000/api/auth/login',
        json=data
    )
    token = resp.json().get("auth_token")
    # beacuse token works for 5 sec we will get "Signature expired" error
    # time.sleep(6) 
    if resp.status_code == 200 and token:
        print("Login successful. Auth token:", token)
        
        # Make the logout request with the token
        logout_resp = requests.post(
            url='http://127.0.0.1:5000/api/auth/logout',
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if logout_resp.status_code == 200:
            print("Logout successful.")
        else:
            print("Logout failed. Response:", logout_resp.text)
    else:
        print("Login failed. Response:", resp.text)

if __name__ == "__main__":
    test_register_with_valid_data()
    print()
    test_register_with_data_already_in_database()
    print()
    test_register_with_invalid_password_with_spaces()
    print()
    test_register_with_inavlid_password()
    print()
    test_login_with_valid_data()
    print()
    test_login_with_invalid_data()
    print()
    test_logout_with_valid_data()