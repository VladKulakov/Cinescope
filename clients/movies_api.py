from constants import MOVIES_ENDPOINT, API_DEV_URl
from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=API_DEV_URl)

    def update_headers(self):
        self._update_session_headers(**{"email": "api1@gmail.com"}, **{"password": "asdqwe123Q"})

    def receiving_post(self,params=None, expected_status=200):
        return self.send_request(method="GET",
                                endpoint=MOVIES_ENDPOINT,
                                expected_status= expected_status,
                                 params = params)

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, generate_movies, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=generate_movies,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )
