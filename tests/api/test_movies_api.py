import allure
import pytest
from utils.data_generator import DataGenerator
from models.base_models import CreatedMoviesResponse, MovieWithReviewsResponse

pytestmark = [pytest.mark.movies, pytest.mark.api]


@allure.epic("Тестирование Movies")
@allure.feature("Тестирование Api")
class TestMovieApi:
    @allure.story("Получение фильмов")
    @pytest.mark.slow
    def test_get_10_movies(self, common_user):
        with allure.step("Получение фильмов и десериализация в словарь"):
            response = common_user.api.movies_api.receiving_post(expected_status=200)
            response_json = response.json()
        with allure.step("Проверяем, что результат не пустой"):
            assert  response_json["movies"]
        with allure.step("Проверяем, что по умолчанию мы получили 10 страниц"):
            assert response_json["pageSize"] == 10

    @allure.epic("Тестирование Movies")
    @allure.story("Получение фильмов")
    @pytest.mark.regression
    def test_get_20_movie(self, common_user):
        size = DataGenerator.pagesize()
        with allure.step(f"Отправляем запрос с параметром {size} фильмов"):
            response = common_user.api.movies_api.receiving_post(params=size,expected_status=200)
        with allure.step("Десериализация ответа в словарь"):
            response_json = response.json()
        with allure.step("Проверяем, что результат не пустой"):
            assert  response_json["movies"]
        with allure.step("Проверяем, что фильмов столько, сколько ожилаем"):
            assert response_json["pageSize"] == size["pageSize"], f"В параметрах установили вывод {size['pageSize']} Афиш!"

    @allure.epic("Тестирование Movies")
    @allure.story("Получение фильмов с фильтрацией price, обычный юзер")
    @pytest.mark.regression
    def test_get_price_filtes(self, common_user):
        min_price, max_price = DataGenerator.price_range().values()
        with allure.step(f"Получение фильмов с мин цена - {min_price} макс цена - {max_price}"):
            response = common_user.api.movies_api.receiving_post(
                                            params={"minPrice": min_price, "maxPrice": max_price},expected_status=200)
        with allure.step("Десериализация ответа в словарь"):
            response_json = response.json()
        with allure.step("Проверяем, что результат не пустой"):
            assert  response_json["movies"]
        with allure.step("Проверяем, что получили 10 фильмов"):
            assert response_json["pageSize"] == 10
        with allure.step("Проверяем все фильмы на соответсвие цены"):
            for number in range(len(response_json['movies'])):
                price = response_json['movies'][number]['price']
                assert min_price <= price <= max_price

    @allure.epic("Тестирование Movies")
    @allure.story("Получение фильмов с фильтрацией по location")
    @pytest.mark.slow
    def test_get_locations(self, common_user):
        locations = DataGenerator.gen_locations()
        response = common_user.api.movies_api.receiving_post(params=locations, expected_status=200)
        response_json = response.json()
        assert  response_json["movies"], "Результат не должен быть пустым!"
        assert response_json["pageSize"] == 10, "По умолчанию Афиш должно быть 10!"
        for number in range(len(response_json['movies'])):
            response_locations = response_json['movies'][number]['location']
            assert response_locations == locations["locations"], "Локация не равна указанной"

    @allure.epic("Тестирование Movies")
    @allure.story("Получение фильмов с некорректной фильтрацией")
    @pytest.mark.slow
    @pytest.mark.parametrize("params,status", [
        (DataGenerator.negative_locations(), 400),
        (DataGenerator.negative_pagesize(), 400),
        (DataGenerator.invalid_price_range(), 400)], ids=["locations", "pageSize", "price_range"])
    def test_get_negative(self, common_user, params, status):
        common_user.api.movies_api.receiving_post(params=params, expected_status=status)

    @allure.epic("Тестирование Movies")
    @allure.story("Повторная фильтрация фильмов с различными параметрами")
    @pytest.mark.flaky(reruns=2, reruns_delay=1)
    @pytest.mark.parametrize("params,expected_status", [
        (DataGenerator.price_range(), 200),
        (DataGenerator.pagesize(), 200),
        (DataGenerator.gen_locations(), 200),
        (DataGenerator.generate_random_genreld(), 200),], ids=["Price", "pageSize", "location", "genreld"])
    def test_filter(self, params, expected_status, api_manager):
         api_manager.movies_api.receiving_post(params=params, expected_status=expected_status)

    @allure.epic("Тестирование Movies")
    @allure.story("Проверка создание фильмов под разными ролями")
    @pytest.mark.regression
    @pytest.mark.parametrize("user,status", [
        ("super_admin", 201),
        ("common_admin", 403),
        ("common_user", 403)])
    def test_create_movies(self, user, status, request, generate_movie):
        user = request.getfixturevalue(user)
        response = user.api.movies_api.create_movie(generate_movie, status)
        if response.status_code == 201:
            response = response.json()
            CreatedMoviesResponse(**response)
            user.api.movies_api.delete_movie(response["id"], 200)

    @allure.epic("Тестирование Movies")
    @allure.story("Проверка создание фильмов под разными ролями")
    @pytest.mark.slow
    @pytest.mark.flaky(reruns=2, reruns_delay=1)
    @pytest.mark.parametrize("user,expected_status", [
    ("super_admin", 200),
    ("common_admin", 200),
    ("common_user", 200)])
    def test_get_movies(self, user, expected_status, request, created_movie_id):
        user = request.getfixturevalue(user)
        response = user.api.movies_api.get_movie(created_movie_id, expected_status)
        response = response.json()
        MovieWithReviewsResponse(**response)

    @allure.epic("Тестирование Movies")
    @allure.story("Проверка удаления фильмов под разными ролями")
    @pytest.mark.regression
    @pytest.mark.flaky(reruns=2, reruns_delay=1)
    @pytest.mark.parametrize("user,expected_status", [
        ("super_admin", 200),
        ("common_admin", 403),
        ("common_user", 403)])
    def test_delete_movies(self, user, request, expected_status, created_movie_id):
        user = request.getfixturevalue(user)
        user.api.movies_api.delete_movie(created_movie_id, expected_status)


@allure.feature("Тестирование синхронности Api и Db")
class TestMovieApiAndBd:
    @allure.epic("Тестирование Movies")
    @pytest.mark.regression
    def test_create_db_movies(self, super_admin, common_user, db_helper, generate_movie_bd):
        movie = db_helper.create_test_movies(generate_movie_bd)
        common_user.api.movies_api.get_movie(movie.id, expected_status=200)
        super_admin.api.movies_api.delete_movie(movie.id, expected_status=200)
        common_user.api.movies_api.get_movie(movie.id, expected_status=404)
        db_resp = db_helper.get_movie_by_id(movie.id)
        assert db_resp is None

    @allure.epic("Тестирование Movies")
    @pytest.mark.regression
    def test_create_api_movies(self, super_admin, creation_user_data, db_helper, generate_movie):
        db_response = db_helper.get_movie_by_name(generate_movie['name'])
        assert db_response is None
        response = super_admin.api.movies_api.create_movie(generate_movie, 201)
        response_json = response.json()
        db_response = db_helper.get_movie_by_name(response_json['name'])
        assert db_response.name == generate_movie['name']
        super_admin.api.movies_api.delete_movie(response_json["id"])
        db_response = db_helper.get_movie_by_name(generate_movie['name'])
        assert db_response is None