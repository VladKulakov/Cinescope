from conftest import test_user


class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True


    def test_get_user_by_locator(self, super_admin, creation_user_data, test_user):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user_info(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user_info(creation_user_data['email']).json()
        print(created_user_response)
        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data['email']
        assert response_by_id.get('fullName') == creation_user_data['fullName']
        assert response_by_id.get('roles', []) == creation_user_data['roles']
        assert response_by_id.get('verified') is True

    def test_get_user_by_id_common_user(self, common_user, test_user):
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)
        print(common_user)
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


