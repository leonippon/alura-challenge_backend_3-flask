from flask_sqlalchemy import SQLAlchemy
from app import create_app
import dotenv
import pytest

@pytest.fixture(scope='session')
def app():

    config = {
        'TESTING': True,
        'FLASK_DEBUG': True,
        'FLASK_ENV': 'testing',
        'ENV_CONF': 'TestingConfig',
        'SECRET_KEY': 'environment_secret_key',
        'LIMIT_ACC': 10000,
        'LIMIT_AG': 100000
    }
    app = create_app(config)


    yield app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='Admin', password=123999):
        return self._client.post('/auth', data={'username': username, 'password': password, 'from_page': 'index'}, follow_redirects=True)

    def logout(self):
        return self._client.get('/logout', follow_redirects=True)


@pytest.fixture
def auth(client):
    return AuthActions(client)