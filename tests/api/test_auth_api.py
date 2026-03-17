from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
import requests

class TestRegistationApi:
    def test_register_user(self, test_user):
        register_url = f'{BASE_URL}{REGISTER_ENDPOINT}'
        response = requests.post(register_url, headers=HEADERS, json=test_user)
        response_json = response.json()
        assert response.status_code == 201, "Ошибка регистрации"
        assert response_json['email'] == test_user['email'], 'Email не совпадает'
        assert 'id' in response_json, 'ID Отсутсвует'
        assert "roles" in response_json, 'Роли не определены'
        assert "USER" in response_json["roles"], 'Роль USER должна быть по умолчанию'


class TestAuthApi:
    def test_authorization_user(self, test_user):
        login_url = f'{BASE_URL}{LOGIN_ENDPOINT}'
        login_json = {'email': test_user['email'], 'password': test_user['password']}
        response = requests.post(login_url, headers=HEADERS, json=login_json)
        response_json = response.json()
        assert response.status_code == 200, "Пользователь не авторизован"
        assert 'accessToken' in response_json, 'Токен отсутствует'
        assert response_json['user']['email'] == test_user['email']


class TestNegative:
    login_url = f'{BASE_URL}{LOGIN_ENDPOINT}'
    def test_nevalid_pass(self, test_user, passwords):
        login_json = {'email': test_user['email'], 'password': passwords}
        response = requests.post(self.login_url, headers=HEADERS, json=login_json)
        assert response.status_code == 401, 'Пользователь авторизован'
        print(f'Тело ответа: {response.text}')

    def test_nevalid_email(self, test_user, email):
        login_json = {'email': email, 'password': test_user['password']}
        response = requests.post(self.login_url, headers=HEADERS, json=login_json)
        assert response.status_code == 401, 'Пользователь авторизован'
        print(f'Тело ответа: {response.text}')

    def test_nevalid_json(self):
        login_json = {}
        response = requests.post(self.login_url, headers=HEADERS, json=login_json)
        assert response.status_code == 401, 'Пользователь авторизован'
        print(f'Тело ответа: {response.text}')