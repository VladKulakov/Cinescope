from custom_requester.custom_requester import CustomRequester
from constants import AUTH_DEV_URL, USER_ENDPOINT

class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_DEV_URL)

    def get_user_info(self, user_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"{USER_ENDPOINT}/{user_id}",
            expected_status=expected_status
        )

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=USER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{USER_ENDPOINT}/{user_id}",
            expected_status=expected_status
        )