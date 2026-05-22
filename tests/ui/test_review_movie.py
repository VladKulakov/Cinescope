import pytest, allure
from playwright.sync_api import Page
from models.ui_page_object.сinescop_review_page import CinescopReviewPage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Movie")
@pytest.mark.ui
class TestFeedbackPage:
    @allure.title("Оставляем отзыв под фильмом")
    def test_feedback_page(self, page: Page, registered_user):
        page = CinescopReviewPage(page)
        page.open_via_auth(registered_user.email, registered_user.password)
        page.all_elements_visibility_check_auth()
        page.fill_review('Отличный фильм на вечер')
        page.check_pop_up_message()

    @allure.title("Проверяем, что без авторизации, не можем оставить отзыв под фильмом")
    def test_feedback_page_not_auth(self, page: Page):
        page = CinescopReviewPage(page)
        page.open()
        page.all_elements_visibility_check_not_auth()
