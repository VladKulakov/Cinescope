import pytest
import requests
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager
from faker import Faker
faker = Faker

@pytest.fixture
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()
    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture
def registered_user(api_manager, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = api_manager.auth_api.register_user(test_user)
    response.password = test_user["password"]
    return response

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


# @pytest.fixture
# def generate_movies(faker):
#     """
#     Генерация movies.
#     """
#     return {
#         "name": f"{faker.unique.word().capitalize()}",
#         "imageUrl": "https://example.com/image.png",
#         "price": faker.random_int(100, 1000),
#         "description": faker.paragraph(1),
#         "location": faker.random_element(elements=["MSK", "SPB"]),
#         "published": True,
#         "genreId": faker.random_int(1, 10)
#    }


# @pytest.fixture(scope="session")
# def requester():
#     """
#     Фикстура для создания экземпляра CustomRequester.
#     """
#     session = requests.Session()
#     return CustomRequester(session=session, base_url=AUTH_DEV_URL)