class TestAuthAPI:
    def test_register_user(self, registered_user, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = registered_user.json()
        assert response["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response, "ID пользователя отсутствует в ответе"
        assert "roles" in response, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response["roles"], "Роль USER должна быть у пользователя"

    def test_login_user(self, authorization_user, test_user):
        """
        Тест на авторизацию пользователя.
        """
        response = authorization_user.json()
        assert "accessToken" in response, "Токен доступа отсутствует в ответе"
        assert response["user"]["email"] == test_user["email"], "Email не совпадает"