class TestAuthAPI:
    def test_register_user(self, api_manager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()
        # Проверки
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager, registered_user, test_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user.json()["email"],
            "password": registered_user.password
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user.json()["email"], "Email не совпадает"
        assert response_data["user"]["roles"] == test_user["roles"], "Роли в ответе не соответствуют зарегистрированным"
        assert "id" in response_data["user"], "ID пользователя отсутствует в ответе"
        login_data = [registered_user.json()["email"], registered_user.password]
        api_manager.auth_api.authenticate(login_data)
        api_manager.user_api.delete_user(registered_user.json()['id'])

    def test_authenticate_delite_user(self, api_manager, registered_user, test_user):
        """
        Тест на авторизацию пользователя и обновление токена, с последующим удалением.
        """
        login_data = [registered_user.json()["email"], registered_user.password]
        api_manager.auth_api.authenticate(login_data)
        api_manager.user_api.delete_user(registered_user.json()['id'])


    def test_negative_scenario(self, api_manager, registered_user, test_user):
        """
        Тест на удаление пользователя без токена в session
        """
        api_manager.user_api.delete_user(registered_user.json()['id'], status=401)
        """
        Тест на получение данных, без прав админа невозможно
        """
        api_manager.user_api.get_user_info(registered_user.json()['id'], status=401)
        """
        Удаление пользователя
        """
        login_data = [registered_user.json()["email"], registered_user.password]
        api_manager.auth_api.authenticate(login_data)
        api_manager.user_api.delete_user(registered_user.json()['id'])
