import pytest
from models.base_models import RegisterUserResponse


class TestUser:
    @pytest.mark.regression
    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        user_model = RegisterUserResponse(**response)
        assert user_model.email == creation_user_data.email
        assert user_model.fullName == creation_user_data.fullName
        assert user_model.roles == creation_user_data.roles
        assert user_model.verified is True

    @pytest.mark.regression
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        user_model = RegisterUserResponse(**created_user_response)
        response_by_id = super_admin.api.user_api.get_user_info(user_model.id).json()
        response_by_email = super_admin.api.user_api.get_user_info(user_model.email).json()
        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('email') == creation_user_data.email
        assert response_by_id.get('fullName') == creation_user_data.fullName
        assert response_by_id.get('roles', []) == creation_user_data.roles
        assert response_by_id.get('verified') is True

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)

    @pytest.mark.regression
    def test_user_db(self, super_admin, creation_user_data, db_helper):
        response = super_admin.api.user_api.create_user(creation_user_data)
        response_json = response.json()
        user_db = db_helper.get_user_by_id(response_json['id'])
        assert user_db.id == response_json['id'] and user_db.email == response_json['email']
        assert db_helper.user_exists_by_email("api1@gmail.com")



#
# import pytest
# from resources.user_creds import SuperAdminCreds
#
#
# @pytest.mark.parametrize("email, password, expected_status", [
#     (f"{SuperAdminCreds.USERNAME}", f"{SuperAdminCreds.PASSWORD}", 200),
#     ("test_login1@email.com", "asdqwe123Q!", 401),  # Сервис не может обработать логин по незареганному юзеру
#     ("", "password", 401),
# ], ids=["Admin login", "Invalid user", "Empty username"])
# def test_login(email, password, expected_status, api_manager):
#     login_data = {
#         "email": email,
#         "password": password
#     }
#     api_manager.auth_api.login_user(login_data=login_data, expected_status=expected_status)


