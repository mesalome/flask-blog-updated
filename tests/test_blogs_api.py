import requests


def test_fetching_blogs_for_authenticated_user():
    data = {
        'username': 'test_user_1',
        'email': 'test@test.com',
        'first_name': 'test',
        'last_name': 'user',
        'password': 'Test123!',
    }


    login_resp = requests.post(
        url='http://127.0.0.1:5000/api/auth/login',
        json=data
    )
    if login_resp.status_code == 200:
        auth_token = login_resp.json().get("auth_token")
        print("Login successful. Auth token:", auth_token)

        headers = {"Authorization": f"Bearer {auth_token}"}

    url = "http://127.0.0.1:5000/api/blog/"

    resp = requests.get(url=url,
                        headers=headers)
    print(resp.json())
import requests

def test_updating_blogs_for_authenticated_user():
    # Login a user and obtain the authentication token
    data = {
        'username': 'test_user_1',
        'email': 'test@test.com',
        'first_name': 'test',
        'last_name': 'user',
        'password': 'Test123!',
    }


    login_resp = requests.post(
        url='http://127.0.0.1:5000/api/auth/login',
        json=data
    )
    if login_resp.status_code == 200:
        auth_token = login_resp.json().get("auth_token")
        print("Login successful. Auth token:", auth_token)

        headers = {"Authorization": f"Bearer {auth_token}"}

        # Specifying the blog post data to create
        post_id = 2
        update_data = {
            'title': 'Updated Title',
            'content': '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                        Aenean ac tristique diam, quis consequat est. Donec hendrerit et justo a rutrum. 
                        Cras imperdiet tempus nisl ac rhoncus. Aliquam fermentum ut urna non auctor. Sed ex orci, 
                        porttitor nec ultricies eget, eleifend vitae felis. Ut euismod orci aliquet nunc eleifend 
                        molestie. Nullam blandit lobortis dapibus.
                        Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. 
                        Donec tincidunt consectetur consequat. Donec auctor interdum vehicula. Proin quis mauris ipsum. 
                        Quisque a purus.''',
        }

        # Send a POST request to update the blog
        url = f"http://127.0.0.1:5000/api/blog/{post_id}/update"
        update_resp = requests.post(url=url, json=update_data, headers=headers)

        if update_resp.status_code == 200:
            print("Blog updated successfully.")
        else:
            print("Failed to update blog. Response:", update_resp.text)
    else:
        print("Login failed. Response:", login_resp.text)

def test_deleting_blogs_for_authenticated_user():
    # Register a user and obtain the authentication token
    data = {
        'username': 'test_user_1',
        'email': 'test@test.com',
        'first_name': 'test',
        'last_name': 'user',
        'password': 'Test123!',
    }


    login_resp = requests.post(
        url='http://127.0.0.1:5000/api/auth/login',
        json=data
    )
    if login_resp.status_code == 200:
        auth_token = login_resp.json().get("auth_token")
        print("Login successful. Auth token:", auth_token)

        headers = {"Authorization": f"Bearer {auth_token}"}

        # Specify the blog data to delete
        post_id = 2  # ID of the blog 

        # POST request to delete the blog
        url = f"http://127.0.0.1:5000/api/blog/{post_id}/delete"
        delte_resp = requests.post(url=url, headers=headers)

        if delte_resp.status_code == 200:
            print("Blog deleted successfully.")
        else:
            print("Failed to delete blog. Response:", delte_resp.text)
    else:
        print("Login failed. Response:", login_resp.text)


def test_creating_blogs_for_authenticated_user():
    # Register a user and obtain the authentication token
    data = {
        'username': 'test_user_1',
        'email': 'test@test.com',
        'first_name': 'test',
        'last_name': 'user',
        'password': 'Test123!',
    }


    login_resp = requests.post(
        url='http://127.0.0.1:5000/api/auth/login',
        json=data
    )
    if login_resp.status_code == 200:
        auth_token = login_resp.json().get("auth_token")
        print("Login successful. Auth token:", auth_token)

        headers = {"Authorization": f"Bearer {auth_token}"}

        # Specify the blog post data to create
        create_data = {
            'title': 'Updated Title',
            'content': '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                        Aenean ac tristique diam, quis consequat est. Donec hendrerit et justo a rutrum. 
                        Cras imperdiet tempus nisl ac rhoncus. Aliquam fermentum ut urna non auctor. Sed ex orci, 
                        porttitor nec ultricies eget, eleifend vitae felis. Ut euismod orci aliquet nunc eleifend 
                        molestie. Nullam blandit lobortis dapibus.
                        Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. 
                        Donec tincidunt consectetur consequat. Donec auctor interdum vehicula. Proin quis mauris ipsum. 
                        Quisque a purus.''',
        }

        # Send a POST request to update the blog
        url = f"http://127.0.0.1:5000/api/blog/create"
        create_resp = requests.post(url=url, json=create_data, headers=headers)

        if create_resp.status_code == 200:
            print("Blog created successfully.")
        else:
            print("Failed to create blog. Response:", create_resp.text)
    else:
        print("Login failed. Response:", login_resp.text)

if __name__ == "__main__":
    test_fetching_blogs_for_authenticated_user()
    test_updating_blogs_for_authenticated_user()
    # test_updating_blogs_for_authenticated_user()
    # test_deleting_blogs_for_authenticated_user()
    # test_creating_blogs_for_authenticated_user()
