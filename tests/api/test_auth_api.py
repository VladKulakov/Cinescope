import datetime
import allure
from pytest_check import check
from clients.api_manager import ApiManager
from constants import Roles
from models.base_models import RegisterUserResponse, TestUser


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):
        response = api_manager.auth_api.register_user(user_data=test_user)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"


    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = [registered_user.email, registered_user.password]
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user.email, "Email не совпадает"
        assert response_data["user"]["roles"] == registered_user.roles, "Роли в ответе не соответствуют зарегистрированным"
        api_manager.auth_api.authenticate(login_data)
        api_manager.user_api.delete_user(registered_user.id)

    def test_authenticate_delite_user(self, api_manager, registered_user):
        """
        Тест на авторизацию пользователя и обновление токена, с последующим удалением.
        """
        login_data = [registered_user.email, registered_user.password]
        api_manager.auth_api.authenticate(login_data)
        api_manager.user_api.delete_user(registered_user.id)


    def test_negative_scenario(self, api_manager, registered_user, test_user):
        """
        Тест на удаление пользователя без токена в session
        """
        api_manager.user_api.delete_user(registered_user.id, expected_status=401)
        """
        Тест на получение данных, без прав админа невозможно
        """
        api_manager.user_api.get_user_info(registered_user.id, expected_status=401)
        """
        Удаление пользователя
        """
        login_data = [registered_user.email, registered_user.password]
        api_manager.auth_api.authenticate(login_data)
        api_manager.user_api.delete_user(registered_user.id)

    @allure.title("Тест регистрации пользователя с помощью Mock")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Ivan Petrovich")
    def test_register_user_mock(self, api_manager: ApiManager, test_user: TestUser, mocker):
        with allure.step(" Мокаем метод register_user в auth_api"):
            mock_response = RegisterUserResponse(  # Фиктивный ответ
                id="id",
                email="email@email.com",
                fullName="INCORRECT_NAME",
                verified=True,
                banned=False,
                roles=[Roles.SUPER_ADMIN],
                createdAt=str(datetime.datetime.now())
            )

            mocker.patch.object(
                api_manager.auth_api,  # Объект, который нужно замокать
                'register_user',  # Метод, который нужно замокать
                return_value=mock_response  # Фиктивный ответ
            )

        with allure.step("Вызываем метод, который должен быть замокан"):
            register_user_response = api_manager.auth_api.register_user(test_user)

        with allure.step("Проверяем, что ответ соответствует ожидаемому"):
            with allure.step("Проверка поля персональных данных"):  # обратите внимание на вложенность allure.step
                with check:
                    # Строка ниже выдаст исклющение и но выполнение теста продолжится
                    check.equal(register_user_response.fullName, "INCORRECT_NAME", "НЕСОВПАДЕНИЕ fullName")
                    check.equal(register_user_response.email, mock_response.email)

            with allure.step("Проверка поля banned"):
                with check("Проверка поля banned"):  # можно использовать вместо allure.step
                    check.equal(register_user_response.banned, mock_response.banned)