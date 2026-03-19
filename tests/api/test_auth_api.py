from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT

class TestAuthAPI:
    def test_register_user(self, requester, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = requester.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=test_user,
            expected_status=201
        )
        response = response.json()
        assert response["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response, "ID пользователя отсутствует в ответе"
        assert "roles" in response, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response["roles"], "Роль USER должна быть у пользователя"


    def test_login_user(self, requester, test_user):
        """
        Тест на авторизацию пользователя.
        """
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=200
        )
        response = response.json()
        assert "accessToken" in response, "Токен доступа отсутствует в ответе"
        assert response["user"]["email"] == test_user["email"], "Email не совпадает"