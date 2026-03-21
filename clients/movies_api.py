from constants import MOVIES_ENDPOINT, BASE_URL
from custom_requester.custom_requester import CustomRequester

class MoviesAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL)


    def update_headers(self, data):
        return self._update_session_headers(**{"username": "api1@gmail.com"}, **{"password": "asdqwe123Q"})


    def receiving_post(self):
        return self.send_request(method="GET",
                                endpoint=MOVIES_ENDPOINT,
                                expected_status= 200)

