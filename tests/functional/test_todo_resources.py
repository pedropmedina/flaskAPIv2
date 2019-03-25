from flask import g, json, url_for

from src.models.todo import Todo

from .test_user_resources import TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD
from .test_user_resources import (
    create_user,
    get_accept_content_type_headers,
    get_authorization_header,
)

TODO_NAME = 'Buy toothpaste'
TODO_CATEGORY = 'Home'


def construct_url(resource_for='many', todo_id=0):
    resource_endpoint = {
        'one': 'api.todo_resource',
        'many': 'api.todo_list_resource',
    }.get(resource_for)

    if resource_for == 'one':
        url = url_for(resource_endpoint, id=todo_id, _external=True)
    else:
        url = url_for(resource_endpoint, _external=True)
    return url


def create_todo(client, token, todo_name, todo_category):
    url = construct_url()
    data = dict(name=TODO_NAME, category=TODO_CATEGORY)
    todo_response = client.post(
        url, headers=get_authorization_header(token), data=json.dumps(data)
    )
    return todo_response


def get_a_todo(client, token, todo_id):
    url = construct_url(resource_for='one', todo_id=todo_id)
    todo_response = client.get(url, headers=get_authorization_header(token))
    return todo_response


def test_get_todos(client):
    '''
    GIVEN a todo
    WHEN (GET) '/api/v1/todos/'
    THEN return todos corresponding to user making request
    '''
    # create user, and use token to make get request
    user_response = create_user(client, TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
    user_response_data = json.loads(user_response.get_data(as_text=True))
    token = user_response_data['message']

    # create todo
    create_todo(client, token, TODO_NAME, TODO_CATEGORY)

    # make GET request with token
    url = construct_url()
    todo_response = client.get(url, headers=get_authorization_header(token))
    todo_response_data = json.loads(todo_response.get_data(as_text=True))['data']

    # assertions
    assert todo_response.status_code == 200
    assert isinstance(todo_response_data, list)
    assert len(todo_response_data) == 1
    assert todo_response_data[0]['name'] == TODO_NAME
    assert todo_response_data[0]['user']['username'] == TEST_USERNAME
    assert todo_response_data[0]['user']['email'] == TEST_EMAIL


def test_create_todo(client):
    '''
    GIVEN the data {name, category}
    WHEN (POST) '/api/v1/todos'
    THEN return todo back to corresponding user
    '''
    # create user to send token in the request header
    user_response = create_user(client, TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
    user_response_data = json.loads(user_response.get_data(as_text=True))
    token = user_response_data['message']
    # make post request to create todo
    todo_response = create_todo(client, token, TODO_NAME, TODO_CATEGORY)
    todo_response_data = json.loads(todo_response.get_data(as_text=True))
    # assert response
    assert todo_response.status_code == 201
    assert todo_response_data['status'] == 'success'


def test_update_todo(client):
    '''
    GIVEN the data to be updated
    WHEN (PATCH) '/api/v1/todos/<id>'
    THEN register changes in db and return todo to corresponding user
    '''
    # create user and to use token in patch request down below
    user_response = create_user(client, TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
    user_response_data = json.loads(user_response.get_data(as_text=True))
    token = user_response_data['message']
    # create todo
    create_todo(client, token, TODO_NAME, TODO_CATEGORY)
    # patch request todo
    url = construct_url(resource_for='one', todo_id=1)
    new_name = 'UPDATED TODO!!!!!!!'
    data = dict(name=new_name)
    updated_todo_response = client.patch(
        url, headers=get_authorization_header(token), data=json.dumps(data)
    )
    updated_todo_response_data = json.loads(
        updated_todo_response.get_data(as_text=True)
    )['data']
    # assert response
    assert updated_todo_response.status_code == 200
    assert updated_todo_response_data['name'] == new_name


def test_delete_todo(client):
    '''
    GIVEN the id
    WHEN (DELETE) '/api/v1/todos/<id>'
    THEN remove todo from db and return success message
    '''
    # we need a user in order to create a todo
    user_response = create_user(client, TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
    user_response_data = json.loads(user_response.get_data(as_text=True))
    token = user_response_data['message']
    # create todo with token from user
    create_todo(client, token, TODO_NAME, TODO_CATEGORY)
    # delete todo with id of 1 as there's only one todo in db
    url = construct_url(resource_for='one', todo_id=1)
    todo_response = client.delete(url, headers=get_authorization_header(token))
    todo_response_data = json.loads(todo_response.get_data(as_text=True))
    # assert code
    assert todo_response.status_code == 200
    assert todo_response_data['status'] == 'success'
