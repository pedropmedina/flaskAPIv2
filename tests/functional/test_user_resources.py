from flask import url_for, json
import jwt

from src.models.user import User
from src.config import secret_key

TEST_USERNAME = 'jamesmadison'
TEST_EMAIL = 'james@email.com'
TEST_PASSWORD = 'Password123!'


def get_accept_content_type_headers():
    '''Test helper to set default headers'''
    return {'Accept': 'application/json', 'Content-Type': 'application/json'}


def get_authorization_header(token=''):
    '''Test helper to set Authorization header'''
    authorization_headers = get_accept_content_type_headers()
    authorization_headers['Authorization'] = f'Bearer {token}'
    return authorization_headers


def create_user(client, username, email, password):
    '''Test helper to create user and return response'''
    url = url_for('api.user_list_resource', _external=True)
    data = dict(username=username, email=email, password=password)
    response = client.post(
        url, headers=get_accept_content_type_headers(), data=json.dumps(data)
    )
    return response


def get_a_user(client, public_id, token):
    '''Test helper to get user a user and return response'''
    # Construct url with user.public_id as argument value.
    # Must set Authorization header in request
    url = url_for('api.user_resource', public_id=public_id, _external=True)
    response = client.get(url, headers=get_authorization_header(token))
    return response


def test_request_without_jwt_authorization(client):
    '''
    GIVEN the Flask app
    WHEN (GET) '/api/v1/users/' with not jwt Authorization header
    THEN ensure we get back 401 Unauthorized request
    '''
    response = client.get(
        url_for('api.user_list_resource'), headers=get_accept_content_type_headers()
    )
    assert response.status_code == 401


def test_create_user(client):
    '''
    GIVEN the Flask app
    WHEN (POST) '/api/v1/users' with username, email, and password
    THEN register new user and response with status code 201
    '''
    user_response = create_user(client, TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
    # get_data(as_text=True) will return a decoded unicode string.
    # Load it with JSON to get back a dictionary
    user_response_data = json.loads(user_response.get_data(as_text=True))
    # get the payload from token
    payload = jwt.decode(
        user_response_data['message'], secret_key, algorithms=['HS256']
    )
    assert user_response.status_code == 201
    assert User.query.count() == 1
    assert user_response_data['status'] == 'success'
    assert isinstance(payload['sub'], int)  # sub should be user.id of type int


def test_get_user(client):
    '''
    GIVEN user.public_id after creating a new user
    WHEN (GET) '/api/v1/users/<public_id>'
    THEN get back the user with status code 200
    '''
    # Create new user, and parse the response
    create_user_response = create_user(client, TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
    create_user_response_data = json.loads(create_user_response.get_data(as_text=True))

    # Grab token from response, decode token and query user with id from token
    token = create_user_response_data['message']
    user_id = User.jwt_decode(token)
    user = User.query.get(user_id)

    # Get specific user and parsed data
    get_user_response = get_a_user(client, public_id=user.public_id, token=token)
    get_user_response_data = json.loads(get_user_response.get_data(as_text=True))[
        'data'
    ]

    assert get_user_response.status_code == 200
    assert get_user_response_data['username'] == user.username
    assert get_user_response_data['email'] == user.email


def test_update_user(client):
    '''
    GIVEN a selected user
    WHEN (PATCH) '/api/v1/users/<public_id>'
    THEN update properties of user and response with status code 200
    '''
    create_user_response = create_user(client, TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
    create_user_response_data = json.loads(create_user_response.get_data(as_text=True))

    token = create_user_response_data['message']
    user_id = User.jwt_decode(token)
    user = User.query.get(user_id)

    url = url_for('api.user_resource', public_id=user.public_id, _external=True)
    data = dict(username='georgewashinton', email='george@gmail.com')
    patch_user_response = client.patch(
        url, headers=get_authorization_header(token), data=json.dumps(data)
    )
    patch_user_response_data = json.loads(patch_user_response.get_data(as_text=True))[
        'data'
    ]
    assert patch_user_response.status_code == 200
    assert patch_user_response_data['username'] == 'georgewashinton'
    assert patch_user_response_data['email'] == 'george@gmail.com'


def test_delete_user(client):
    '''
    GIVEN the requested user
    WHEN (DELETE) '/api/v1/users/<public_id>'
    THEN delete user from db and return status code 204
    '''
    create_user_response = create_user(client, TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
    create_user_response_data = json.loads(create_user_response.get_data(as_text=True))

    token = create_user_response_data['message']
    user_id = User.jwt_decode(token)
    user = User.query.get(user_id)

    url = url_for('api.user_resource', public_id=user.public_id, _external=True)
    delete_user_response = client.delete(url, headers=get_authorization_header(token))
    assert delete_user_response.status_code == 204
