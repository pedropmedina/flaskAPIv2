from src.models.user import User
from src import bcrypt


def test_new_user(new_user):
    '''
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, username fields are defined correctly
    '''
    assert new_user.username == 'jamesadams'
    assert new_user.email == 'james@gmail.com'
    assert new_user.check_password(password='pass123')
    assert len(new_user.todos) == 0
