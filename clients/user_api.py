from custom_requester.custom_requester import CustomRequester
from constants import AUTH_DEV_URL

class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_DEV_URL)

    def get_user_info(self, user_id, status=200):
        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_id}",
            expected_status=status
        )

    def delete_user(self, user_id, status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"/user/{user_id}",
            expected_status=status
        )