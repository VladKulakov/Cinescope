from constants import BASE_URL, HEADERS, LOGIN_ENDPOINT, REGISTER_ENDPOINT
from utils.data_generator import DataGenerator
import requests
import pytest

@pytest.fixture(scope="session")
def test_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()
    return {"email": random_email,
            "fullName": random_name,
            "password": random_password,
            "passwordRepeat": random_password,
            "roles": ["USER"]}

@pytest.fixture(scope="session")
def auth_session(test_user):
    session = requests.session()
    session.headers.update(HEADERS)
    register_url = f'{BASE_URL}{REGISTER_ENDPOINT}'
    response_create = session.post(register_url, json=test_user)
    assert response_create.status_code == 201, "Учетная запись не создана"
    login_url = f'{BASE_URL}{LOGIN_ENDPOINT}'
    login_data = {'email': test_user['email'],
                  'password': test_user['password']}
    response_login = session.post(login_url, json=login_data)
    assert response_login.status_code == 200, "Ошибка авторизации"
    token = response_login.json().get("accessToken")
    assert token is not None, "Нет токена доступа"
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture()
def email():
    return DataGenerator.generate_random_email()

@pytest.fixture()
def passwords():
    return DataGenerator.generate_random_password()