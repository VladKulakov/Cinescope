from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT, AUTH_DEV_URL
from custom_requester.custom_requester import CustomRequester

class AuthAPI(CustomRequester):
    """
      Класс для работы с аутентификацией.
      """

    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_DEV_URL)

    def register_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, data, expected_status=200):
        login_data = {
            "email": data[0],
            "password": data[1]
        }
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, user_creds):
        response = self.login_user(user_creds).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")
        token = response["accessToken"]
        self._update_session_headers(**{"authorization": "Bearer " + token})
