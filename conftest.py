import time
import pytest
import requests
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds
from entities.user import User
from constants import Roles
from models.base_models import TestUser, RegisterUserResponse, CreatedMoviesResponse
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from typing import Generator, Callable
from db_requester.db_helpers import DBHelper

@pytest.fixture #была добавлена в файл conftest.py
def delay_between_retries():
    time.sleep(2)  # Задержка в 2 секунды\ это не обязательно но
    yield          # нужно понимать что такая возможность имеется


@pytest.fixture(scope="function")
def created_test_user(db_helper):
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)


@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="module")
def db_session() -> Generator[Session, None, None]:
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="session")
def session()-> Generator[requests.Session, None, None]:
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session) -> ApiManager:
    return ApiManager(session)

@pytest.fixture
def user_session() -> Generator[Callable[[], ApiManager], None, None]:
    user_pool = []
    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session
    yield _create_user_session
    for user in user_pool:
        user.close_session()

@pytest.fixture
def common_admin(user_session, super_admin, creation_user_data) -> User:
    new_session = user_session()
    common_admin = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_session)
    super_admin.api.user_api.create_user(creation_user_data)
    common_admin.api.auth_api.authenticate(common_admin.creds)
    return common_admin

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data) -> User:
    new_session = user_session()
    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session)
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def super_admin(user_session) -> User:
    new_session = user_session()
    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)
    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()
    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )

@pytest.fixture
def creation_user_data(test_user):
    test_user.verified = True
    test_user.banned = False
    return test_user

@pytest.fixture
def registered_user(api_manager, test_user) -> RegisterUserResponse:
    response = api_manager.auth_api.register_user(test_user)
    user_response = RegisterUserResponse(**response.json())
    user_response.password = test_user.password
    return user_response

@pytest.fixture
def generate_movie():
    return DataGenerator.generate_movies()

@pytest.fixture
def generate_movie_bd():
    return DataGenerator.generate_movies_data()

@pytest.fixture
def created_movie_id(super_admin, generate_movie):
    response = super_admin.api.movies_api.create_movie(generate_movie, 201)
    response_json = response.json()
    model_movie = CreatedMoviesResponse(**response_json)
    movie_id = model_movie.id
    yield movie_id
    try:
        super_admin.api.movies_api.delete_movie(movie_id, 200)
    except ValueError as e:
        if "404" not in str(e):
            raise

